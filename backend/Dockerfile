############################################
# 1️⃣  Build stage – Maven + JDK 17
############################################
FROM eclipse-temurin:17-jdk-focal AS builder

WORKDIR /app

# ── 1. Copy build files first (better cache) ──
COPY .mvn/ .mvn
COPY mvnw pom.xml ./
RUN chmod +x mvnw \
    && ./mvnw -B dependency:go-offline      # download all deps

# ── 2. Copy source and build the fat JAR ──
COPY src ./src
RUN ./mvnw -B package -DskipTests           # creates target/<app>.jar


############################################
# 2️⃣  Runtime stage – slim JRE 17
############################################
FROM eclipse-temurin:17-jre-focal

# (optional) run as non‑root for safety
RUN useradd -ms /bin/bash spring
USER spring

WORKDIR /app
COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8080

# ── 3. Start Spring Boot ──
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
