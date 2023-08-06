FROM python:3.8-slim

COPY dist/*.whl /

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
        jq \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# hadolint ignore=DL3013
RUN pip --no-cache-dir install /*.whl

CMD ["tuxbuild", "--help"]
