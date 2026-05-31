from agents import manager, ingenier, analiser
from crewai import Task, Crew, Process


task1 = Task(
    agent = manager,
    description = "Збери RAW дані: перевір відкриті порти, системних юзерів, запущені служби та стан фаєрволу. Поверни тільки зібрані дані без аналізу.",
    expected_output = "Список: відкриті порти, активні юзери, служби, статус фаєрволу"
)


task2 = Task(
    agent = analiser,
    description = "На основі зібраних RAW даних визнач: які порти небезпечні, чи є підозрілі юзери, які служби зайві. Розстав пріоритети: критичний/середній/низький.",
    expected_output = "Таблиця загроз з пріоритетами: критичний, середній, низький"
)



task3 = Task(
    agent = manager,
    description = "Склади фінальний звіт на основі аналізу загроз. Дай конкретні рекомендації що виправити. Збережи звіт через save_results.",
    expected_output = "Структурований звіт з розділами: знайдені проблеми, рекомендації, висновок"
)


crew = Crew(
    agents = [manager, ingenier, analiser],
    tasks = [task1, task2, task3],
    process = Process.sequential
)


print(crew.kickoff())