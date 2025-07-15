# Network Traffic Congestion Prediction System Design

## Key Changes from Reference Implementation

1. **Architecture**:
   - Class-based implementation for better organization
   - Strict separation of concerns (ML logic, web layer, assets)
   - Type hints throughout for better code quality

2. **Machine Learning**:
   - Replaced RandomForest with GradientBoostingClassifier
   - Added new features (peak_hour_flag, packet_size_variance)
   - Improved feature naming for clarity

3. **Infrastructure**:
   - Docker containerization support
   - Environment variables for configuration
   - Production-ready Gunicorn server

4. **Monitoring & Alerts**:
   - Email alerts for high-probability congestion
   - Comprehensive logging with loguru

5. **Frontend**:
   - Modern dashboard with visualization
   - Real-time prediction interface
   - Protocol filtering controls

## Performance Considerations

- Maintained ≥90% accuracy requirement
- GradientBoostingClassifier chosen for similar accuracy to original
- Feature engineering optimized for performance

## API Compatibility

Maintained `/predict` endpoint with same input/output format:

**Request**:
```json
{
    "duration": 10.5,
    "src_bytes": 1024,
    "dst_bytes": 2048,
    "count": 5,
    "srv_count": 3,
    "hour": 9
}