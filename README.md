# Vi-TCM Explorer: Topological Data Analysis for Traditional Medicine

## Overview

This repository contains the official source code and datasets for the paper: **"Knowledge-Driven Topological Data Analysis in Traditional Medicine: A Macroscopic Synergy Approach"** (Accepted/Submitted to MIWAI 2026).

**Vi-TCM Explorer** is a web-based platform that utilizes Topological Data Analysis (TDA) and Graph Neural Networks (GNNs) to quantify and predict synergistic effects in traditional Vietnamese herbal formulations. It extracts the topological shape (Betti-1 loops) from a Tripartite Knowledge Graph to identify multi-target pharmacological mechanisms.

## Repository Structure (Microservices)

- /backend - FastAPI server utilizing giotto-tda for real-time Persistent Homology calculations. (Deployed on Hugging Face Spaces).
- /frontend - React/Next.js interactive UI for TM practitioners. (Deployed on Vercel).
- /data - Digitized records from the Vietnamese Pharmacopoeia (Do Tat Loi).
- /notebooks - Original Jupyter Notebooks for graph extraction and Betti Curve vectorization.

## Deployment

- **Backend (TDA Engine):** Deployed on Hugging Face Spaces using Docker.
- **Frontend (Web UI):** Deployed on Vercel.

## Citation

If you use this code or dataset in your research, please cite our paper:

@inproceedings{vo2026knowledge,  
title={Knowledge-Driven Topological Data Analysis in Traditional Medicine: A Macroscopic Synergy Approach},  
author={Vo, Thi Kim Anh},  
booktitle={},  
year={2026}  
}
