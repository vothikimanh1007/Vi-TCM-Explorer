from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import networkx as nx
import numpy as np
from gtda.graphs import GraphGeodesicDistance
from gtda.homology import VietorisRipsPersistence
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Vi-TCM Topological Engine API", version="1.0.0")

# Enable CORS for Frontend (Vercel) integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to your Vercel domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class Formulation(BaseModel):
    herbs: List[str]

# --- 1. Load / Mock Knowledge Graph ---
# In production, this loads from data/ViThuoc_final.csv
G = nx.Graph()
# Mock data for demonstration purposes
mock_edges = [
    ('Ginseng', 'Sweet'), ('Ginseng', 'Warm'), ('Ginseng', 'Spleen'), ('Ginseng', 'Lung'),
    ('Astragalus', 'Sweet'), ('Astragalus', 'Warm'), ('Astragalus', 'Lung'),
    ('Angelica', 'Sweet'), ('Angelica', 'Warm'), ('Angelica', 'Liver'), ('Angelica', 'Heart'),
    ('Licorice', 'Sweet'), ('Licorice', 'Heart'), ('Licorice', 'Spleen')
]
G.add_edges_from(mock_edges)

@app.get("/")
def read_root():
    return {"status": "online", "message": "Vi-TCM TDA Engine is running."}

@app.post("/api/synergy")
async def calculate_synergy(formulation: Formulation):
    """
    Calculates the topological synergy of an herbal formulation using Persistent Homology.
    """
    try:
        # 1. Extract 1-hop subgraph based on requested herbs
        sub_nodes = set(formulation.herbs)
        for herb in formulation.herbs:
            if herb in G.nodes:
                sub_nodes.update(G.neighbors(herb))
        
        subgraph = G.subgraph(sub_nodes)
        
        if len(subgraph.nodes) < 3:
            return {"synergy_score": 0, "betti_1_loops": 0, "message": "Insufficient nodes for topology."}

        # 2. Transform to Adjacency Matrix
        adj_matrix = nx.to_numpy_array(subgraph)
        
        # 3. Geodesic Distance Matrix
        ggd = GraphGeodesicDistance(directed=False, unweighted=True)
        X_distance = ggd.fit_transform([adj_matrix])
        
        # 4. Persistent Homology Computation (H0 and H1)
        vr = VietorisRipsPersistence(metric='precomputed', homology_dimensions=[0, 1])
        diagrams = vr.fit_transform(X_distance)
        diagram = diagrams[0]
        
        # 5. Extract Betti-1 features (Cycles/Loops = Synergy)
        h1_features = diagram[diagram[:, 2] == 1]
        betti_1_count = len(h1_features)
        
        # Calculate Synergy Score (0-100) based on loop density
        score = min(100, (betti_1_count * 15) + 40)
        
        return {
            "requested_herbs": formulation.herbs,
            "subgraph_nodes": len(subgraph.nodes),
            "betti_0_components": len(diagram[diagram[:, 2] == 0]),
            "betti_1_loops": betti_1_count,
            "synergy_score": round(score, 1),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
