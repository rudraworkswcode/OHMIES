from fastapi import FastAPI, HTTPException
from supabase import create_client, Client

app = FastAPI(
    title="Smart Grid Electricity Insights API",
    description="Real-time behavioral clustering and explainable energy-saving recommendations API.",
    version="1.0.0"
)

# --- SUPABASE CONFIGURATION ---
SUPABASE_URL = "https://fsyvkfwrzfcpmxcjhnty.supabase.co"       
SUPABASE_KEY = "sb_publishable__B3C4K42ow8DaXIBq20FQg_zQFtnCy9"  
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Smart Grid Energy Insights API is running locally on VS Code!"}

@app.get("/api/insights/{customer_id}")
def get_customer_insight(customer_id: str):
    """
    Fetch real-time user profile, technical limits, usage metrics, 
    and explainable AI saving recommendations for a given customer ID.
    """
    # 1. Query user profile (Fixed column name to 'customer_id')
    user_res = supabase.table("users").select("*").eq("customer_id", customer_id).execute()
    if not user_res.data:
        raise HTTPException(status_code=404, detail=f"Customer ID '{customer_id}' not found.")
    
    user = user_res.data[0]
    user_uuid = user['id']

    # 2. Query corresponding usage metrics
    metrics_res = supabase.table("usage_metrics").select("*").eq("user_id", user_uuid).execute()
    metrics = metrics_res.data[0] if metrics_res.data else {}

    # 3. Query cluster behavioral insights & rule engine recommendations
    insights_res = supabase.table("cluster_insights").select("*").eq("user_id", user_uuid).execute()
    insight_data = insights_res.data[0] if insights_res.data else {}

    # 4. Construct unified response payload
    return {
        "customer_id": user['customer_id'],
        "consumer_type": user['consumer_type'],
        "profile_category": user['profile_category'],
        "max_connected_load_kw": user['max_connected_load_kw'],
        "usage_metrics": {
            "avg_daily_usage_kwh": metrics.get("avg_daily_usage_kwh"),
            "peak_to_average_ratio": metrics.get("peak_to_average_ratio")
        },
        "behavioral_cluster": {
            "cluster_id": insight_data.get("cluster_id"),
            "cluster_label": insight_data.get("cluster_label"),
            "actionable_recommendation": insight_data.get("explainable_insight")
        }
    }

@app.get("/api/cluster-summary")
def get_cluster_summary():
    """
    Fetch aggregate statistics for portfolio-wide cluster distribution.
    """
    insights_res = supabase.table("cluster_insights").select("cluster_id, cluster_label").execute()
    data = insights_res.data
    
    summary = {}
    for item in data:
        label = item['cluster_label']
        summary[label] = summary.get(label, 0) + 1

    return {
        "total_analyzed_consumers": len(data),
        "cluster_distribution": summary
    }