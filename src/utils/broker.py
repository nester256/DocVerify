from taskiq import PrometheusMiddleware
from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker("amqp://guest:guest@rabbitmq:5672/").with_middlewares(PrometheusMiddleware(server_port=9000))
