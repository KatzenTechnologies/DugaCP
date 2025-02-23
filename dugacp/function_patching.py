from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, Callable, List, Optional, Union, Set
from enum import Enum

# ================== Перечисление режимов выполнения ==================
class PatchExecutionMode(Enum):
    SEQUENTIAL = 1  # Последовательное выполнение (по умолчанию)
    PARALLEL = 2    # Параллельное выполнение (через ThreadPoolExecutor)
    CONDITIONAL = 3 # Условное выполнение (останавливается при False)
    PIPELINE = 4    # Пайплайн (результат передается следующему хуку)
    AGGREGATE = 5   # Агрегация результатов всех хуков

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