# shellcheck disable=SC2164
cd src
uvicorn catalogservice.app:app --reload
