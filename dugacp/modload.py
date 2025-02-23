import os
import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Callable, List, Optional, Union, Set
import logging
from dugacp.function_patching import *
import json


# ================== Класс для управления зависимостями ==================
class ModDependencyManager:
    def __init__(self):
        self.dependencies: Dict[str, Set[str]] = {}  # Зависимости модов
        self.incompatibilities: Dict[str, Set[str]] = {}  # Несовместимости модов
        self.loaded_mods: Set[str] = set()  # Загруженные моды

    def add_dependency(self, mod_id: str, required_mod: str):
        """Добавляет зависимость для мода"""
        if mod_id not in self.dependencies:
            self.dependencies[mod_id] = set()
        self.dependencies[mod_id].add(required_mod)

    def add_incompatibility(self, mod_id: str, incompatible_mod: str):
        """Добавляет несовместимость для мода"""
        if mod_id not in self.incompatibilities:
            self.incompatibilities[mod_id] = set()
        self.incompatibilities[mod_id].add(incompatible_mod)

    def check_dependencies(self, mod_id: str, dependencies: List[str]) -> bool:
        """Проверяет, удовлетворены ли зависимости мода"""
        for dep in dependencies:
            if dep not in self.loaded_mods:
                return False
        return True

    def check_incompatibilities(self, mod_id: str, incompatibilities: List[str]) -> bool:
        """Проверяет, есть ли несовместимые моды"""
        for incomp in incompatibilities:
            if incomp in self.loaded_mods:
                return False
        return True

    def register_loaded_mod(self, mod_id: str):
        """Регистрирует загруженный мод"""
        self.loaded_mods.add(mod_id)

# ================== Класс для управления модами ==================
class ModManager:
    def __init__(self, game_api, mods_dir: str = "mods", game_dir: str = "game", log_file: str = "mods.log"):
        self.game_api = game_api  # Сохраняем API игры внутри менеджера
        self.mods_dir = Path(mods_dir)
        self.game_dir = Path(game_dir)
        self.log_file = Path(log_file)
        self.loaded_mods: Dict[str, Any] = {}
        self.function_registry: Dict[str, Callable] = {}
        self.function_patches: Dict[str, FunctionPatch] = {}
        self.function_factories: List[Callable] = {}
        self.game_modules: Dict[str, Any] = {}
        self.dependency_manager = ModDependencyManager()

        # Настройка логирования
        self._setup_logging()

        # Добавляем папку игры в sys.path
        sys.path.append(str(self.game_dir))

        # Создаем папки, если их нет
        self.mods_dir.mkdir(exist_ok=True)
        self.game_dir.mkdir(exist_ok=True)

    def _setup_logging(self):
        """Настройка логирования в файл"""
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        self.logger = logging.getLogger("ModManager")

    def get_mod_logger(self, mod_id: str):
        """Возвращает логгер для конкретного мода"""
        return logging.getLogger(f"ModManager.{mod_id}")

    def _read_manifest(self, mod_folder: Path) -> Optional[Dict[str, Any]]:
        """Чтение manifest.json из папки мода"""
        manifest_file = mod_folder / "manifest.json"
        if manifest_file.exists():
            try:
                with open(manifest_file, "r", encoding="utf-8") as file:
                    manifest = json.load(file)
                    if "id" not in manifest:
                        print(f"Мод '{mod_folder.name}' не имеет поля 'id' в manifest.json и будет пропущен")
                        return None
                    return manifest
            except json.JSONDecodeError as e:
                print(f"Ошибка чтения manifest.json в моде '{mod_folder.name}': {e}")
        return None

    def load_mods(self):
        """Загрузка всех модов из директории"""
        for mod_folder in self.mods_dir.iterdir():
            if mod_folder.is_dir():  # Проверяем, что это папка
                try:
                    # Читаем manifest.json
                    manifest = self._read_manifest(mod_folder)
                    if not manifest:
                        continue

                    mod_id = manifest["id"]  # Уникальный идентификатор мода

                    # Проверяем зависимости
                    dependencies = manifest.get("dependencies", [])
                    if not self.dependency_manager.check_dependencies(mod_id, dependencies):
                        print(f"Мод '{mod_id}' не загружен: не удовлетворены зависимости")
                        continue

                    # Проверяем несовместимости
                    incompatibilities = manifest.get("incompatibilities", [])
                    if not self.dependency_manager.check_incompatibilities(mod_id, incompatibilities):
                        print(f"Мод '{mod_id}' не загружен: обнаружены несовместимые моды")
                        continue

                    # Добавляем папку мода в sys.path для импорта
                    sys.path.append(str(mod_folder))

                    # Загружаем основной скрипт мода
                    spec = importlib.util.spec_from_file_location(
                        f"{mod_id}.mod", mod_folder / "mod.py"
                    )
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    self.loaded_mods[mod_id] = mod  # Регистрируем мод по ID
                    self.dependency_manager.register_loaded_mod(mod_id)

                    if hasattr(mod, "apply_mod"):
                        # Передаем логгер, API игры и путь к папке мода (как строку)
                        mod_logger = self.get_mod_logger(mod_id)
                        mod.apply_mod(self, mod_logger, self.game_api, str(mod_folder))
                        print(f"Mod '{mod_id}' успешно загружен")

                    # Убираем папку мода из sys.path после загрузки
                    sys.path.remove(str(mod_folder))

                except Exception as e:
                    print(f"Ошибка загрузки мода '{mod_folder.name}': {str(e)}")
                    sys.path.remove(str(mod_folder))  # Убираем папку в случае ошибки

        # Применяем фабрики функций после загрузки всех модов
        self._apply_function_factories()

    def _apply_function_factories(self):
        """Применение всех зарегистрированных фабрик функций"""
        for factory in self.function_factories:
            try:
                new_functions = factory(self)
                if new_functions:
                    for func in new_functions:
                        self.register_function(func)
            except Exception as e:
                print(f"Ошибка в фабрике функций: {str(e)}")

    def register_function(self, func: Callable):
        """Регистрация функций для модификации"""
        self.function_registry[func.__name__] = func
        return func

    def register_function_factory(self, factory: Callable):
        """Регистрация фабрики функций"""
        self.function_factories.append(factory)
        return factory

    def patch_function(self, target_func: Union[str, Callable]) -> FunctionPatch:
        """Создание патча для функции"""
        if isinstance(target_func, str):
            func = self.function_registry.get(target_func)
            if not func:
                raise ValueError(f"Функция {target_func} не зарегистрирована")
        else:
            func = target_func

        if func.__name__ in self.function_patches:
            return self.function_patches[func.__name__]

        patch = FunctionPatch(func)
        self.function_patches[func.__name__] = patch
        return patch

    def apply_modification(
            self,
            target_func: Union[str, Callable],
            *,
            pre_hook: Callable = None,
            post_hook: Callable = None,
            replace: Callable = None,
            modifiers: List[Callable] = None
    ):
        """Применение модификаций к целевой функции"""
        patch = self.patch_function(target_func)

        if pre_hook:
            patch.add_pre_hook(pre_hook)
        if post_hook:
            patch.add_post_hook(post_hook)
        if replace:
            patch.replace(replace)
        if modifiers:
            for m in modifiers:
                patch.add_post_hook(m)

        return patch