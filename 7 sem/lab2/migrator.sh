#!/bin/bash

if [ -d "/Applications/Postgres.app/Contents/Versions/latest/bin" ]; then
    export PATH="/Applications/Postgres.app/Contents/Versions/latest/bin:$PATH"
elif [ -d "/Applications/Postgres.app/Contents/Versions/17/bin" ]; then
    export PATH="/Applications/Postgres.app/Contents/Versions/17/bin:$PATH"
fi

# Параметры подключения к базе данных
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5433}"
DB_NAME="${DB_NAME:-dsilabs}"
DB_USER="${DB_USER:-postgres}"
DB_PASSWORD="${DB_PASSWORD:-2004egor}"

# Путь к директории с SQL-скриптами миграций
MIGRATIONS_DIR="$(pwd)"

# Функция для выполнения SQL-запросов из файла
run_sql() {
    local file_name="$1"
    export PGPASSWORD="$DB_PASSWORD"
    psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -f "$file_name" -q
}

# Функция для выполнения SQL-запроса из строки
run_sql_c() {
    local sql_query="$1"
    export PGPASSWORD="$DB_PASSWORD"
    psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -c "$sql_query" -q
}

# Получение списка примененных миграций
get_applied_migrations() {
    export PGPASSWORD="$DB_PASSWORD"
    psql -U "$DB_USER" -d "$DB_NAME" -h "$DB_HOST" -p "$DB_PORT" -t -c "SELECT migration_name FROM migrations ORDER BY applied_at;" 2>/dev/null
}

# Запись информации о примененной миграции
record_migration() {
    local migration_name="$1"
    local escaped_name=$(printf "%q" "$migration_name")
    run_sql_c "INSERT INTO migrations (migration_name) VALUES ('$escaped_name');"
}

# Основная функция применения миграций
apply_migrations() {
    # Получаем список уже примененных миграций
    local applied_migrations=$(get_applied_migrations)
    
    # Находим все .sql файлы в директории
    local sql_files=$(find "$MIGRATIONS_DIR" -maxdepth 1 -name "*.sql" -type f | sort)
    
    # Перебираем все .sql файлы
    while IFS= read -r sql_file; do
        if [[ -z "$sql_file" ]]; then
            continue
        fi
        
        # Получаем имя файла без пути
        local migration_name=$(basename "$sql_file")
        
        # Проверяем, была ли миграция уже применена
        if echo "$applied_migrations" | grep -q "^[[:space:]]*$(printf "%q" "$migration_name")[[:space:]]*$"; then
            echo "Миграция $migration_name уже применена. Пропускаем."
        else
            echo "Применение миграции: $migration_name"
            if run_sql "$sql_file"; then
                record_migration "$migration_name"
                echo "Миграция $migration_name успешно применена"
            else
                echo "Ошибка применения миграции $migration_name"
                exit 1
            fi
        fi
    done <<< "$sql_files"
}

# Главная функция
main() {
    # Создаем таблицу migrations если она не существует
    create_migrations_table
    
    # Применяем миграции
    apply_migrations
    
    echo "Мигратор завершил работу"
}

# Запускаем основную функцию
main "$@"