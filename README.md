# Flask MySQL Application con Docker y CI/CD

Esta aplicación demuestra una implementación completa de una aplicación web Flask con MySQL (master-slave), Nginx como balanceador de carga y un pipeline CI/CD usando GitHub Actions.

## Características

- Aplicación Flask con endpoints REST para CRUD de usuarios
- Base de datos MySQL con configuración master-slave
- Nginx como balanceador de carga
- Pipeline CI/CD con GitHub Actions
- Despliegue automático a VM
- Exposición del servicio mediante ngrok

## Requisitos Previos

- Docker Desktop
- Git
- Cuenta de GitHub
- Máquina Virtual para despliegue
- Cuenta de ngrok

## Instalación Local

1. Clonar el repositorio:
```bash
git clone <url-repositorio>
cd <nombre-repositorio>
```

2. Iniciar la aplicación:
```bash
docker-compose up --build
```

## Endpoints

- GET `/`: Verificar estado de la aplicación
- GET `/users`: Obtener lista de usuarios
- POST `/users`: Crear nuevo usuario
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com"
  }
  ```

## Configuración CI/CD

1. Configurar secrets en GitHub:
   - DOCKER_HUB_USERNAME
   - DOCKER_HUB_TOKEN
   - VM_HOST
   - VM_USERNAME
   - VM_SSH_KEY
   - NGROK_AUTH_TOKEN

2. Push a la rama main para activar el despliegue automático

## Pruebas

```bash
# Crear usuario
curl -X POST http://localhost/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "email": "john@example.com"}'

# Obtener usuarios
curl http://localhost/users
```

## Mantenimiento

```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Verificar replicación MySQL
docker-compose exec db_slave mysql -uroot -proot -e "SHOW SLAVE STATUS\G"
```

## Licencia

MIT
