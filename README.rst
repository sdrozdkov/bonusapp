BonusApp
**********

Simple bonus app with some business logic and passwordless authentication.

Usage
-----

Pre-required Setup:

Hit below command to start server on port 8080.

.. code:: shell

    git clone https://github.com/sdrozdkov/bonusapp
    cd bonusapp
    docker-compose build
    docker-compose up
    
Provision some users, if you want add users, check out *app/api/v1/provision.py*

.. code:: shell
    
    curl -i -X POST -H "Content-Type: application/json" http://localhost:8080/api/v1/provision


Now you can try login:

1st step: send email address to login endpoint:

.. code:: shell

    curl -i -X POST -H "Content-Type: application/json" http://localhost:8080/api/v1/login -d '{"email":"bundieboss@gmail.com"}'

    HTTP/1.1 200 OK
    Content-Type: application/json
    Set-Cookie: sess_token=sYUd9eybXkjB1BYBmp7fjgeaxnde8tcSSsS7mRXmzXu3a5G047; Expires=Wed, 29-Aug-2018 20:31:05 GMT; Max-Age=300; Path=/
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    Content-Length: 42
    Date: Wed, 29 Aug 2018 20:26:05 GMT

    {
      "result": {
        "message": "ok"
      }
    }


2nd step: use "sess_token" to validate your email code, in my example sess_token value is "sYUd9eybXkjB1BYBmp7fjgeaxnde8tcSSsS7mRXmzXu3a5G047"

.. code:: shell

    curl -i -X POST -H "Content-Type: application/json" --cookie "sess_token=sYUd9eybXkjB1BYBmp7fjgeaxnde8tcSSsS7mRXmzXu3a5G047" http://localhost:8080/api/v1/login/validate -d '{"code":"2628"}'

    HTTP/1.1 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    Set-Cookie: session=eyJzZXNzaWQiOiIyRk1ZcU9HYldlOVM0cmhaazUzSktjd0hDdG4weGRoNXVTT2Y2Z3VmVFpGcjNHVGtJbCJ9.DmiWcg.DUvTvKUrPZ_FCJN0DDKSHeSuYW4; HttpOnly;  Path=/
    Content-Length: 42
    Date: Wed, 29 Aug 2018 20:41:22 GMT

    {
      "result": {
        "message": "ok"
      }
    }    

now you authenticated and can use "session" cookie to another requests


check your profile

.. code:: shell
    
    curl -i -X GET --cookie "session=eyJzZXNzaWQiOiIyRk1ZcU9HYldlOVM0cmhaazUzSktjd0hDdG4weGRoNXVTT2Y2Z3VmVFpGcjNHVGtJbCJ9.DmiWcg.DUvTvKUrPZ_FCJN0DDKSHeSuYW4" http://localhost:8080/api/v1/profile
    
    HTTP/1.1 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    Content-Length: 121
    Date: Wed, 29 Aug 2018 20:43:33 GMT

    {
      "result": {
        "bonus_card": "111",
        "email": "bundieboss@gmail.com",
        "full_name": "Sergey Drozdkov"
      }
    }


Change BONUS_CARD_NUMBER value with your "bonus_card_ filed from profile in scripts/trx_generator.py and than generate amount test bonus transactions

.. code:: shell

    python scripts/trx_generator.py



check your bonus transaction history

.. code:: shell

    curl -i -X GET --cookie "session=eyJzZXNzaWQiOiIyRk1ZcU9HYldlOVM0cmhaazUzSktjd0hDdG4weGRoNXVTT2Y2Z3VmVFpGcjNHVGtJbCJ9.DmiWcg.DUvTvKUrPZ_FCJN0DDKSHeSuYW4" 'http://localhost:5000/api/v1/profile/history'
    
    HTTP/1.1 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    Content-Length: 1957
    Date: Wed, 29 Aug 2018 22:29:31 GMT
    
    {
      "result": {
        "page": 1,
        "total_pages": 10,
        "transactions": [
          {
            "arrival_airport": "PLK",
            "departure_airport": "VKO",
            "flight_date": "2018-12-10T19:30:00",
            "trx_id": "101",
            "trx_value": 10
          },
          {
            "arrival_airport": "PLK",
            "departure_airport": "VKO",
            "flight_date": "2018-09-12T04:33:15",
            "trx_id": "100",
            "trx_value": 58
          },
    ...
          {
            "arrival_airport": "PLK",
            "departure_airport": "VKO",
            "flight_date": "2018-09-13T17:33:45",
            "trx_id": "110",
            "trx_value": 25
          }
        ]
      }
    }


Use page data from response to paginating over history

.. code:: shell

    curl -i -X GET --cookie "session=eyJzZXNzaWQiOiIyRk1ZcU9HYldlOVM0cmhaazUzSktjd0hDdG4weGRoNXVTT2Y2Z3VmVFpGcjNHVGtJbCJ9.DmiWcg.DUvTvKUrPZ_FCJN0DDKSHeSuYW4" 'http://localhost:5000/api/v1/profile/history?page=9'

    HTTP/1.1 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Access-Control-Allow-Credentials: true
    Content-Length: 1956
    Date: Wed, 29 Aug 2018 22:28:25 GMT
    
    {
      "result": {
        "page": 9,
        "total_pages": 10,
        "transactions": [
          {
            "arrival_airport": "PLK",
            "departure_airport": "VKO",
            "flight_date": "2018-09-06T04:33:48",
            "trx_id": "181",
            "trx_value": 8
          },
          {
            "arrival_airport": "PLK",
            "departure_airport": "VKO",
            "flight_date": "2018-09-12T01:33:48",
            "trx_id": "182",
            "trx_value": 11
          },
    ...
          {
            "arrival_airport": "PLK",
            "departure_airport": "VKO",
            "flight_date": "2018-09-03T00:33:49",
            "trx_id": "190",
            "trx_value": 6
          }
        ]
      }
    }
