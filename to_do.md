# 🐳 DOCKER_TEST_PLAN.md
## 🧪 CI Test Suite To-Do List

### 1. Dockerize Server & Client
- [ ] Create Dockerfiles for server and client binaries
- [ ] Mount config files and test assets via volumes
- [ ] Expose required ports
- [ ] Define startup commands

### 2. Create Docker Network
- [ ] Set up custom bridge network
- [ ] Assign static IPs or hostnames
- [ ] Enable container name resolution

### 3. Update Localhost Tests
- [ ] keepp `localhost` and add   Docker hostname
- [ ] Use real socket communication
- [ ] Validate connection via TCP/UDP

### 4. Enable Log Parsing
- [ ] Redirect stdout/stderr to log files
- [ ] Read and assert logs in Python tests
- [ ] Add verbosity or log flags to binaries

### 5. Complete Remote Test Case
- [ ] Use `client_remote.cfg` with Docker IP
- [ ] Simulate latency or packet loss
- [ ] Validate retry and timeout handling

### 6. CI Integration & Cleanup
- [ ] Add teardown steps for containers and volumes
- [ ] Integrate with GitHub Actions or GitLab CI
- [ ] Use a test runner to orchestrate all cases
