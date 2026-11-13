# OFL-008: Initial Architecture Decision Record

## Overview

This document outlines the proposed technical foundation for OpenFinanceLab's initial release, prioritizing tools that fit the project scope, are accessible to the team, and can be used without paid services.

## 1. Frontend

**Decision:** Use React with TypeScript and Vite.

**Reasoning:**
- React supports building interactive UI components, while TypeScript adds static type checking.
- Vite provides a fast development server and frontend build tooling.

**Trade-off:** Requires familiarity with React and TypeScript, but offers a flexible, well-supported ecosystem.

## 2. Backend

**Decision:** Use Python with FastAPI.

**Reasoning:**
- Python supports the CSV processing and financial calculations needed for the application.
- FastAPI provides API endpoints, request validation, file uploads, and automatic documentation.

**Trade-off:** Introduces a framework to learn and maintain. Keeping processing logic separate from the API helps limit complexity.

## 3. Database

**Decision:** Use PostgreSQL.

**Reasoning:**
- Supports structured financial data, relationships, and complex queries.
- Free, open source, and available for local development.

**Trade-off:** Requires more setup than SQLite, which does not need a separate database server.

## 4. Testing

**Backend: pytest**

**Reasoning:** Provides readable tests, fixtures, and parameterization for testing CSV parsing, data validation, and financial calculations.

**Trade-off:** Requires an additional dependency compared to Python's built-in unittest framework.

**Frontend: Vitest and React Testing Library**

**Reasoning:** Vitest integrates with Vite, while React Testing Library supports testing component behavior through user interactions.

**Trade-off:** Vitest has a smaller ecosystem than Jest, but integrates more naturally with Vite.

**End-to-end: Playwright (later)**

Playwright can test complete browser workflows, such as uploading a CSV and viewing financial results.

**Trade-off:** Requires additional setup and maintenance, so it can be introduced after the main workflow is implemented.

## 5. Frontend Deployment

**Decision:** Use Vercel for frontend hosting and preview deployments.

**Reasoning:**
- GitHub integration supports automatic deployments and preview URLs for pull requests.
- Shared previews make it easier for the team to review changes without running the frontend locally.

**Trade-off:** Vercel only hosts the frontend. The backend and database require separate environments, and the frontend will need to connect to an accessible backend.

## 6. Development Setup

The frontend, backend, and database can run locally during development. Vercel provides hosted frontend deployments, while the backend and database will need separate local or hosted environments.

## Summary

- **Frontend:** React, TypeScript, Vite
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Backend testing:** pytest
- **Frontend testing:** Vitest, React Testing Library
- **End-to-end testing:** Playwright (later)
- **Frontend deployment:** Vercel