# Guía de setup — Entorno de desarrollo en Windows

## Requisitos previos (instalar en orden)

### 1. Git
- Descargar: https://git-scm.com/download/win
- Durante la instalación: seleccionar "Git from the command line and also from 3rd-party software"
- Verificar: `git --version`

### 2. Flutter SDK
- Descargar Flutter 3.32.0 desde: https://docs.flutter.dev/get-started/install/windows
- Extraer en `C:\flutter` (sin espacios en la ruta)
- Agregar `C:\flutter\bin` al PATH del sistema:
  - Win + R → `sysdm.cpl` → Variables de entorno → Path → Nuevo → `C:\flutter\bin`
- Verificar: `flutter --version`

### 3. Android Studio
- Descargar: https://developer.android.com/studio
- Durante la instalación: incluir Android SDK, Android Emulator, Android Virtual Device
- Abrir Android Studio → SDK Manager → instalar:
  - Android SDK Platform 36 (API 36)
  - Android Emulator
  - Intel x86_64 Atom System Image (o ARM si la PC tiene chip ARM)
- Configurar variable de entorno `ANDROID_HOME`:
  - Ruta típica: `C:\Users\<usuario>\AppData\Local\Android\Sdk`
  - Agregar también al PATH: `%ANDROID_HOME%\platform-tools`

### 4. Java JDK (requerido por Android)
- Android Studio trae su propio JDK (recomendado)
- Configurar: `JAVA_HOME` → `C:\Program Files\Android\Android Studio\jbr`
- Agregar al PATH: `%JAVA_HOME%\bin`

### 5. VS Code (editor)
- Descargar: https://code.visualstudio.com/
- Instalar extensiones:
  - Flutter (de Dart Code)
  - Dart (de Dart Code)

### 6. Docker Desktop
- Descargar: https://www.docker.com/products/docker-desktop
- Habilitar WSL 2 backend durante la instalación
- Verificar: `docker --version` y `docker-compose --version`

### 7. Node.js (para el backend NestJS)
- Descargar Node.js LTS: https://nodejs.org/
- Verificar: `node --version` y `npm --version`

---

## Verificación del entorno

```bash
flutter doctor
```

Todos los checkmarks deben estar en verde (salvo Xcode, que es solo macOS). Si alguno falla, seguir las instrucciones del propio `flutter doctor`.

---

## Clonar los proyectos

```bash
git clone <url-repo-backend>       jennygas-app-backend
git clone <url-repo-app-cliente>   jennygas-app-cliente
git clone <url-repo-app-chofer>    jennygas-app-chofer
git clone <url-repo-lib>           jennygas_lib
git clone <url-repo-admin>         garrafitas_admin
```

Mantener todos en la misma carpeta raíz (por ejemplo `C:\proyectos\garrafitas\`), ya que las apps usan dependencia de path relativa `../jennygas_lib`.

---

## Levantar el backend (NestJS + Docker)

### Terminal 1 — Base de datos y Redis

```bash
cd jennygas-app-backend
docker-compose up -d
```

Verificar que los contenedores estén corriendo:
```bash
docker ps
```
Deben aparecer `garrafitas_db` (PostgreSQL) y `garrafitas_redis` (Redis).

### Terminal 2 — Servidor NestJS

```bash
cd jennygas-app-backend
npm install
npm run start:dev
```

El servidor queda escuchando en `http://localhost:3000/api`.
Swagger disponible en `http://localhost:3000/api/docs`.

---

## Crear y lanzar el emulador Android

En Android Studio:
1. Device Manager → Create Virtual Device
2. Seleccionar: Pixel 8 (o cualquier phone)
3. System Image: API 36 x86_64
4. Finish → Play (▶)

O desde terminal:
```bash
flutter emulators --launch Pixel_8
```

---

## Correr las apps (dos terminales separadas)

> **Importante:** En el emulador Android, el backend local se accede como `10.0.2.2:3000`, no como `localhost`. Las apps ya están configuradas con eso.

### Terminal 3 — App Cliente (Android)

```bash
cd jennygas-app-cliente
flutter pub get
flutter run -d emulator-5554
```

### Terminal 4 — App Chofer (Android)

Si solo hay un emulador Android disponible, crear un segundo emulador en Android Studio con otro nombre (ej: `Pixel_8_Chofer`), lanzarlo y luego:

```bash
cd jennygas-app-chofer
flutter pub get
flutter run -d emulator-5556
```

Para ver el ID del emulador corriendo:
```bash
flutter devices
```

---

## Levantar el entorno de trabajo (flujo diario)

Cada vez que querés trabajar con las apps, seguí estos pasos en orden.

### Paso 1 — Backend (Terminal 1)

```bash
cd jennygas-app-backend
docker-compose up -d
npm run start:dev
```

> Si falla con error de contraseña de base de datos:
> ```bash
> docker-compose down
> # Borrar carpeta postgres\ del proyecto
> docker-compose up -d
> npm run start:dev
> ```

### Paso 2 — Levantar el emulador Android

```bash
flutter emulators --launch Pixel_8
```

Esperá que esté listo antes de continuar:
```bash
adb devices   # tiene que mostrar "device", no "offline"
```

### Paso 3 — App Cliente (Terminal 2)

En Windows solo hay emuladores Android (no iOS Simulator). Ambas apps corren en Android.

```bash
cd jennygas-app-cliente
flutter run -d emulator-5554 --release
```

### Paso 4 — App Chofer (Terminal 3)

Si usás el mismo emulador para las dos apps, las instala como apps separadas sin problema.

```bash
cd jennygas-app-chofer
flutter run -d emulator-5554 --release
```

> Se usan dos terminales al mismo tiempo. Cada `flutter run` queda activo mientras desarrollás.

---

### URLs del backend configuradas

| App | Dispositivo | URL del backend |
|-----|-------------|-----------------|
| App Cliente | Android Emulator | `http://10.0.2.2:3000/api/` |
| App Chofer | Android Emulator | `http://10.0.2.2:3000/api/` |

> `10.0.2.2` es cómo el emulador Android llega al `localhost` de tu PC.

---

## Comandos útiles durante el desarrollo

| Acción | Comando |
|--------|---------|
| Hot reload | Presionar `r` en la terminal donde corre `flutter run` |
| Hot restart | Presionar `R` en la terminal donde corre `flutter run` |
| Ver dispositivos disponibles | `flutter devices` |
| Ver emuladores disponibles | `flutter emulators` |
| Ver logs del backend | `docker logs garrafitas_db` |
| Parar Docker | `docker-compose down` |
| Reiniciar DB (borrar datos) | `docker-compose down` → borrar carpeta `postgres/` → `docker-compose up -d` |

---

## Diferencia macOS vs Windows para el backend local

| Dispositivo | URL del backend |
|-------------|-----------------|
| iOS Simulator (solo macOS) | `http://localhost:3000/api/` |
| Android Emulator | `http://10.0.2.2:3000/api/` |
| Dispositivo físico Android | IP local de la PC (ej: `http://192.168.1.x:3000/api/`) |

---

## Notas para dispositivo físico

Si querés correr en un teléfono Android real conectado por USB:
1. Habilitar "Opciones de desarrollador" en el teléfono (tocar 7 veces el número de build)
2. Activar "Depuración USB"
3. Conectar con cable
4. `flutter devices` debe mostrar el teléfono
5. Cambiar la `baseUrl` en `api_client.dart` a la IP local de la PC (ver con `ipconfig`)
