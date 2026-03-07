rm /tmp/.canopy/.sessions/test-123.json

cat > test-input.json << 'EOF'
{
  "session_id": "test-123",
  "cwd": "/tmp/test",
  "hook_event_name": "BeforeTool",
  "tool_name": "write_file",
  "tool_input": {
    "file_path": "test.txt",
    "content": "Test content"
  }
}
EOF
cat test-input.json | env/bin/python -m canopy_mcp example_policy.toml --hook
echo "Exit code: $?"

cat test-input.json | env/bin/python -m canopy_mcp example_policy.toml --hook
echo "Exit code: $?"


rm test-input.json
rm /tmp/.canopy/.sessions/test-123.json