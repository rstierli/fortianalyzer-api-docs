# SD-WAN Audio MOS Quality Monitoring

Retrieve SD-WAN interface Mean Opinion Score (MOS) for voice quality analysis.

> **✅ All code examples tested:** Verified against FortiAnalyzer v7.4.8, v7.6.4, v8.0.0.

## Overview

This endpoint retrieves SD-WAN audio MOS (Mean Opinion Score) quality metrics - useful for:
- Monitoring voice call quality over SD-WAN links
- VoIP and UC application performance analysis
- SLA validation for voice services (Microsoft Teams, Zoom, etc.)
- Identifying degraded audio quality before users complain
- SD-WAN link selection for real-time applications
- Codec performance comparison

MOS scores range from 1 (poor) to 5 (excellent), measuring perceived voice quality.

This endpoint uses the **two-step asynchronous pattern**. See the workflow below for complete details.

## Endpoint Details

**Method:** `POST`
**URL:** `/jsonrpc`
**API Path (Step 1):** `/fortiview/adom/{adom}/sdwan-intf-mos-line/run/`
**API Path (Step 2):** `/fortiview/adom/{adom}/sdwan-intf-mos-line/run/{tid}`
**ADOM Support:** Yes
**Requires Authentication:** Yes
**Minimum Version:** 7.4.0

## Prerequisites

- Active session or valid API key
- Read access to FortiView data in specified ADOM
- SD-WAN feature enabled on FortiGate devices
- Voice/UC traffic monitoring enabled
- MOS measurement configured on SD-WAN interfaces

## Request Example

`````{tab-set}
````{tab-item} REQUEST
```json
{
    "method": "add",
    "params": [{
        "url": "/fortiview/adom/root/sdwan-intf-mos-line/run/",
        "apiver": 3,
        "case-sensitive": false,
        "device": [{
            "devid": "All_FortiGate"
        }],
        "filter": "moscodec=g711",
        "limit": 10,
        "sort-by": [],
        "time-range": {
            "start": "2024-11-10 13:17",
            "end": "2024-11-10 14:17"
        }
    }],
    "session": "{{session_id}}",
    "id": 1
}
```
````
````{tab-item} RESPONSE
```json
{
    "result": [{
        "data": {
            "tid": 12469
        },
        "status": {
            "code": 0,
            "message": "OK"
        }
    }]
}
```
````
`````

## Complete Python Example

```python
import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_sdwan_mos_quality(session_id, adom, time_range, codec_filter="g711"):
    """
    Get SD-WAN MOS quality metrics for voice traffic

    Args:
        session_id: Active session ID
        adom: ADOM name
        time_range: Time range dict with 'start' and 'end'
        codec_filter: Audio codec filter (g711, g729, opus, etc.)

    Returns:
        list: MOS quality data points
    """
    url = "https://faz.example.com/jsonrpc"

    # Submit task
    payload = {
        "method": "add",
        "params": [{
            "url": f"/fortiview/adom/{adom}/sdwan-intf-mos-line/run/",
            "apiver": 3,
            "filter": f"moscodec={codec_filter}",
            "time-range": time_range
        }],
        "session": session_id,
        "id": 1
    }

    response = requests.post(url, json=payload, verify=False)
    tid = response.json()['result'][0]['data']['tid']

    # Poll for results
    while True:
        poll_payload = {
            "method": "get",
            "params": [{
                "url": f"/fortiview/adom/{adom}/sdwan-intf-mos-line/run/{tid}"
            }],
            "session": session_id,
            "id": 2
        }

        response = requests.post(url, json=poll_payload, verify=False)
        data = response.json()['result'][0]['data']

        if data['status'] == 'done' and data['percentage'] == 100:
            return data.get('mos_data', [])

        time.sleep(2)

# Example
mos_data = get_sdwan_mos_quality(
    session_id="your_session_id",
    adom="root",
    time_range={"start": "2024-11-10 13:00", "end": "2024-11-10 14:00"},
    codec_filter="g711"
)

for dp in mos_data:
    print(f"Interface: {dp['interface']} | MOS: {dp['mos_score']:.2f}")
```

## MOS Score Interpretation

| MOS Range | Quality | User Experience | Recommendation |
|-----------|---------|-----------------|----------------|
| 4.0-5.0 | Excellent | Crystal clear | Ideal for business voice |
| 3.5-4.0 | Good | Minor imperfections | Acceptable for most use |
| 3.0-3.5 | Fair | Noticeable issues | Monitor closely |
| 2.5-3.0 | Poor | Annoying quality | Investigate immediately |
| <2.5 | Bad | Unusable | Critical issue |

## Common Audio Codecs

- **G.711**: HD voice (64kbps) - Highest quality
- **G.729**: Compressed (8kbps) - Lower bandwidth
- **Opus**: Adaptive codec used by Teams, WebRTC
- **G.722**: Wideband audio

## Related Endpoints

- [SD-WAN Interface Statistics](./create-task-sd-wan-interface-bandwidth-line.md) - Interface metrics
- [SD-WAN Applications](./create-task-sd-wan-application.md) - Application usage
- [Fetch Results by Task ID](./fetch-result-by-task-id.md) - Retrieve results

---

**Last Updated:** 2025-11-09
**API Version:** 7.6.4+
