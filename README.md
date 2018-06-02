# taskFromSOLab
Реализовать веб-сервис с REST-api, которому можно передать URL произвольной веб-страницы,
и получить статистику по количеству используемых на этой веб-странице тегов в формате json.

При этом нужно реализовать этот веб-сервис как очередь задач - то есть в ответ на запрос с
url нужно вернуть uuid задачи, задачу поставить в очередь, и иметь возможность по uuid задачи 
получить результат ее выполнения.

*****************************************
API сервиса состоит из следующих методов:
POST        v1/task
GET        v1/task
*****************************************
POST v1/task
************
Запрос:
{
    "url":  "https://yandex.ru/"
}
*******
Ответ:
{
    "task_uuid": "<UUID>"
}
  
******************************************* 
  GET v1/task
 ********
Запрос:
{
    "task_uuid": “<UUID>”
}
*******    
В запросе передаем <UUID> задачи.
********
Ответ:
{
    "status": "<STATUS>"
    "result": ... 
}
