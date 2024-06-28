# Estágio 1: Construção
FROM python:3.10 as builder

# Configura variáveis de ambiente para não escrever bytecode e não colocar logs em buffer
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instala dependências para construir pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libgdk-pixbuf2.0-dev \
    shared-mime-info \
    fonts-liberation \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria um diretório de trabalho
WORKDIR /software

# Copia os requisitos para o contêiner
COPY requirements.txt .

# Instala virtualenv e dependências do projeto sem inserir cache
RUN pip install --no-cache-dir virtualenv \
    && virtualenv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Estágio 2: Execução
FROM python:3.10

# Configura variáveis de ambiente para não escrever bytecode e não colocar logs em buffer
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Cria um diretório de trabalho
WORKDIR /software

# Cria um usuário não-root com permissões 1000:1000 e adiciona ele ao grupo
RUN addgroup --gid 1000 vkgroup && adduser --disabled-password --gecos "" --uid 1000 --gid 1000 vkuser

# Copia o ambiente virtual do estágio de construção
COPY --from=builder /opt/venv /opt/venv

# Copia o código do projeto para o diretório de trabalho
COPY . .

# Define as permissões para o usuário não-root no workspace
RUN chown -R vkuser:vkgroup /software

# Troca para o usuário não-root
USER vkuser

# Adiciona o virtualenv ao PATH
ENV PATH="/opt/venv/bin:$PATH"

# Exponha a porta do container
EXPOSE 8000

# Comando padrão para iniciar o contêiner
CMD uvicorn src.application.api.main:app --workers 1 --host 0.0.0.0 --port 8000
