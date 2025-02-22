import os
import importlib
import sys
from pathlib import Path
from typing import Dict, Any, Callable, List, Optional, Union, Set
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================== Перечисление режимов выполнения ==================
class PatchExecutionMode(Enum):
    SEQUENTIAL = 1  # Последовательное выполнение (по умолчанию)
    PARALLEL = 2    # Параллельное выполнение (через ThreadPoolExecutor)
    CONDITIONAL = 3 # Условное выполнение (останавливается при False)
    PIPELINE = 4    # Пайплайн (результат передается следующему хуку)
    AGGREGATE = 5   # Агрегация результатов всех хуков

# ================== Класс для управления зависимостями ==================
class ModDependencyManager:
    def __init__(self):
        self.dependencies: Dict[str, Set[str]] = {}  # Зависимости модов
        self.incompatibilities: Dict[str, Set[str]] = {}  # Несовместимости модов
        self.loaded_mods: Set[str] = set()  # Загруженные моды

    def add_dependency(self, mod_name: str, required_mod: str):
        """Добавляет зависимость для мода"""
        if mod_name not in self.dependencies:
            self.dependencies[mod_name] = set()
        self.dependencies[mod_name].add(required_mod)

    def add_incompatibility(self, mod_name: str, incompatible_mod: str):
        """Добавляет несовместимость для мода"""
        if mod_name not in self.incompatibilities:
            self.incompatibilities[mod_name] = set()
        self.incompatibilities[mod_name].add(incompatible_mod)

    def check_dependencies(self, mod_name: str) -> bool:
        """Проверяет, удовлетворены ли зависимости мода"""
        if mod_name not in self.dependencies:
            return True
        return all(dep in self.loaded_mods for dep in self.dependencies[mod_name])

    def check_incompatibilities(self, mod_name: str) -> bool:
        """Проверяет, есть ли несовместимые моды"""
        if mod_name not in self.incompatibilities:
            return True
        return not any(incomp in self.loaded_mods for incomp in self.incompatibilities[mod_name])

    def register_loaded_mod(self, mod_name: str):
        """Регистрирует загруженный мод"""
        self.loaded_mods.add(mod_name)

# ================== Класс для патчинга функций ==================
class FunctionPatch:
    def __init__(self, target_func: Callable):
        self.target_func = target_func
        self.original_func = target_func
        self.pre_hooks: List[Callable] = []
        self.post_hooks: List[Callable] = []
        self.replace_func: Optional[Callable] = None
        self.enabled = True
        self.pre_mode = PatchExecutionMode.SEQUENTIAL
        self.post_mode = PatchExecutionMode.SEQUENTIAL

    def __call__(self, *args, **kwargs):
        if not self.enabled:
            return self.original_func(*args, **kwargs)

        # Применение pre-хуков
        modified_args, modified_kwargs = self._execute_hooks(
            self.pre_hooks, self.pre_mode, *args, **kwargs
        )

        # Вызов оригинальной или замененной функции
        if self.replace_func:
            result = self.replace_func(*modified_args, **modified_kwargs)
        else:
            result = self.original_func(*modified_args, **modified_kwargs)

        # Применение post-хуков
        final_result = self._execute_hooks(
            self.post_hooks, self.post_mode, result, *modified_args, **modified_kwargs
        )[0]  # Возвращаем только результат

        return final_result

    def _execute_hooks(
        self,
        hooks: List[Callable],
        mode: PatchExecutionMode,
        *args,
        **kwargs
    ) -> Any:
        """Выполнение хуков в зависимости от режима"""
        if not hooks:
            return args, kwargs

        if mode == PatchExecutionMode.SEQUENTIAL:
            return self._execute_sequential(hooks, *args, **kwargs)
        elif mode == PatchExecutionMode.PARALLEL:
            return self._execute_parallel(hooks, *args, **kwargs)
        elif mode == PatchExecutionMode.CONDITIONAL:
            return self._execute_conditional(hooks, *args, **kwargs)
        elif mode == PatchExecutionMode.PIPELINE:
            return self._execute_pipeline(hooks, *args, **kwargs)
        elif mode == PatchExecutionMode.AGGREGATE:
            return self._execute_aggregate(hooks, *args, **kwargs)
        else:
            raise ValueError(f"Unknown execution mode: {mode}")

    def _execute_sequential(self, hooks: List[Callable], *args, **kwargs):
        """Последовательное выполнение хуков"""
        modified_args = args
        modified_kwargs = kwargs.copy()
        for hook in hooks:
            result = hook(*modified_args, **modified_kwargs)
            if isinstance(result, tuple) and len(result) == 2:
                modified_args, modified_kwargs = result
        return modified_args, modified_kwargs

    def _execute_parallel(self, hooks: List[Callable], *args, **kwargs):
        """Параллельное выполнение хуков"""
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(hook, *args, **kwargs)
                for hook in hooks
            ]
            results = [f.result() for f in as_completed(futures)]
        return args, kwargs  # Параллельные хуки не изменяют аргументы

    def _execute_conditional(self, hooks: List[Callable], *args, **kwargs):
        """Условное выполнение хуков"""
        modified_args = args
        modified_kwargs = kwargs.copy()
        for hook in hooks:
            result = hook(*modified_args, **modified_kwargs)
            if not result:
                break
            if isinstance(result, tuple) and len(result) == 2:
                modified_args, modified_kwargs = result
        return modified_args, modified_kwargs

    def _execute_pipeline(self, hooks: List[Callable], *args, **kwargs):
        """Пайплайн: результат передается следующему хуку"""
        result = args[0] if args else None
        for hook in hooks:
            result = hook(result)
        return (result,), kwargs

    def _execute_aggregate(self, hooks: List[Callable], *args, **kwargs):
        """Агрегация результатов всех хуков"""
        results = [hook(*args, **kwargs) for hook in hooks]
        return results, kwargs

    def set_pre_execution_mode(self, mode: PatchExecutionMode):
        """Установка режима выполнения pre-хуков"""
        self.pre_mode = mode
        return self

    def set_post_execution_mode(self, mode: PatchExecutionMode):
        """Установка режима выполнения post-хуков"""
        self.post_mode = mode
        return self

    def add_pre_hook(self, hook: Callable):
        """Добавление pre-хука"""
        self.pre_hooks.append(hook)
        return self

    def add_post_hook(self, hook: Callable):
        """Добавление post-хука"""
        self.post_hooks.append(hook)
        return self

    def replace(self, new_func: Callable):
        """Замена оригинальной функции"""
        self.replace_func = new_func
        return self

    def enable(self):
        """Включение патча"""
        self.enabled = True
        return self

    def disable(self):
        """Отключение патча"""
        self.enabled = False
        return self

    def restore(self):
        """Восстановление оригинальной функции"""
        self.replace_func = None
        self.pre_hooks.clear()
        self.post_hooks.clear()
        return self

# ================== Класс для управления модами ==================
class ModManager:
    def __init__(self, mods_dir: str = "mods", game_dir: str = "game"):
        self.mods_dir = Path(mods_dir)
        self.game_dir = Path(game_dir)
        self.loaded_mods: Dict[str, Any] = {}
        self.function_registry: Dict[str, Callable] = {}
        self.function_patches: Dict[str, FunctionPatch] = {}
        self.function_factories: List[Callable] = {}
        self.game_modules: Dict[str, Any] = {}  # Загруженные модули игры
        self.dependency_manager = ModDependencyManager()
        
        # Добавляем папку игры в sys.path для импорта
        sys.path.append(str(self.game_dir))

        # Создаем папки, если их нет
        self.mods_dir.mkdir(exist_ok=True)
        self.game_dir.mkdir(exist_ok=True)

    def load_game_module(self, module_name: str):
        """Динамически загружает модуль игры"""
        if module_name not in self.game_modules:
            try:
                module = importlib.import_module(module_name)
                self.game_modules[module_name] = module
                print(f"Модуль игры '{module_name}' успешно загружен")
            except ImportError as e:
                print(f"Ошибка загрузки модуля игры '{module_name}': {e}")
        return self.game_modules.get(module_name)

    def get_game_module(self, module_name: str) -> Optional[Any]:
        """Возвращает загруженный модуль игры"""
        return self.game_modules.get(module_name)

    def load_mods(self):
        """Загрузка всех модов из директории"""
        mod_files = list(self.mods_dir.glob("*.py"))
        mod_files.sort()  # Сортируем для предсказуемого порядка загрузки

        for mod_file in mod_files:
            if mod_file.name.startswith("_"):
                continue  # Игнорируем служебные файлы
                
            mod_name = mod_file.stem
            try:
                # Проверяем зависимости и несовместимости
                if not self.dependency_manager.check_dependencies(mod_name):
                    print(f"Mod '{mod_name}' не загружен: не удовлетворены зависимости")
                    continue
                if not self.dependency_manager.check_incompatibilities(mod_name):
                    print(f"Mod '{mod_name}' не загружен: обнаружены несовместимые моды")
                    continue

                # Загружаем мод
                spec = importlib.util.spec_from_file_location(
                    f"mods.{mod_name}", mod_file
                )
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.loaded_mods[mod_name] = mod
                self.dependency_manager.register_loaded_mod(mod_name)
                
                if hasattr(mod, "apply_mod"):
                    mod.apply_mod(self)
                    print(f"Mod '{mod_name}' успешно загружен")
                    
            except Exception as e:
                print(f"Ошибка загрузки мода {mod_name}: {str(e)}")

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