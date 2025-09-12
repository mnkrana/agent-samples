# Run this only one time

import vertexai
from vertexai import agent_engines
from tool_agent.agent import root_agent

PROJECT_ID = "agents-demo-471909"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://agents-demo"

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)

remote_app = agent_engines.create(
    agent_engine=app,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]"   
    ]
)

print(f"Deployment finished!")
print(f"Resource Name: {remote_app.resource_name}")
# Resource Name: projects/754673837740/locations/us-central1/reasoningEngines/7103236541572448256