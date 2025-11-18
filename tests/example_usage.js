// Example: Using your MCP server from JavaScript/Node.js
// (Not just OpenAI SDK!)

const MCP_URL = "https://YOUR-NGROK-URL.ngrok-free.app/mcp";

async function callMCPTool(toolName, arguments = {}) {
  const response = await fetch(MCP_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: toolName,
        arguments: arguments
      }
    })
  });
  
  return await response.json();
}

// Example usage
(async () => {
  console.log("Calling get_resume_info...");
  const result = await callMCPTool("get_resume_info");
  console.log(JSON.stringify(result, null, 2));
  
  console.log("\nCalling get_skills...");
  const skills = await callMCPTool("get_skills", { min_weight: 8 });
  console.log(JSON.stringify(skills, null, 2));
})();
