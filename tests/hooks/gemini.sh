rm ~/.canopy/.sessions/test-123.json

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

did_fail=0

env/bin/python -m canopy_mcp example_policy.toml --hook < test-input.json
exit_code=$?
if [ "$exit_code" -ne 2 ]; then
    echo "FAIL"
    did_fail=1
fi

env/bin/python -m canopy_mcp example_policy.toml --hook < test-input.json
exit_code=$?
if [ "$exit_code" -ne 2 ]; then
    echo "FAIL"
    did_fail=1
fi

rm test-input.json
rm ~/.canopy/.sessions/test-123.json

exit $did_fail