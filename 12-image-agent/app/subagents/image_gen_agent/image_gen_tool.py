from google import genai
from google.genai import types
from google.adk.tools import ToolContext

async def generate_images(imagen_prompt: str, tool_context: ToolContext):

    client = genai.Client().aio
    try:

        response = await client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=imagen_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
                safety_filter_level="block_low_and_above",
                person_generation="allow_adult",
            ),
        )        
        if response.generated_images is not None:
            for generated_image in response.generated_images:
                # Get the image bytes
                image_bytes = generated_image.image.image_bytes
                counter = str(tool_context.state.get("loop_iteration", 0))
                artifact_name = f"generated_image_" + counter + ".png"

                # Save as ADK artifact (optional, if still needed by other ADK components)
                report_artifact = types.Part.from_bytes(
                    data=image_bytes, mime_type="image/png"
                )

                await tool_context.save_artifact(artifact_name, report_artifact)
                print(f"Image also saved as ADK artifact: {artifact_name}")

                return {
                    "status": "success",
                    "message": f"Image generated .  ADK artifact: {artifact_name}.",
                    "artifact_name": artifact_name,
                }
        else:
            # model_dump_json might not exist or be the best way to get error details
            error_details = str(response)  # Or a more specific error field if available
            print(f"No images generated. Response: {error_details}")
            return {
                "status": "error",
                "message": f"No images generated. Response: {error_details}",
            }

    except Exception as e:
        error_message = f"Image generation failed: {e}" 
        print(error_message) # Print to the console for full logging
        return {"status": "error", "message": error_message}