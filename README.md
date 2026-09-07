# ⚡ Smart Attendance — AI-Powered Facial Recognition Frontend

<div align="center">

[![React](https://img.shields.io/badge/React-18.3.1-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.8.3-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.4.19-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4.17-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![shadcn/ui](https://img.shields.io/badge/shadcn%2Fui-Radix_Primitives-000000?style=for-the-badge&logo=radix-ui&logoColor=white)](https://ui.shadcn.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth_%26_PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)

<br/>

**A next-generation automated attendance and classroom management interface powered by real-time computer vision, deep facial embeddings, and instant WhatsApp parent notifications.**

[Key Features](#-key-features) • [Tech Stack](#-technology-stack) • [Quick Start](#-quick-start) • [Environment Config](#-environment-variables) • [Route & Role Matrix](#-application-routes--role-matrix) • [Architecture](#-architecture--directory-structure)

</div>

---

## 🌟 Key Features

### 👁️ Real-Time Face Recognition Attendance
* **Live Camera Stream Processing**: Scans classroom video streams in real-time, detecting multi-face bounding boxes and identities instantly.
* **Cropped Face Pipeline**: Sends detected face crops to the InsightFace AI backend for low-latency embedding matching.
* **Liveness & Anti-Spoofing Detection**: Highlights recognized students in vibrant green boxes while flagging spoof or unregistered faces.
* **Manual Override**: Quick-toggle manual marking in case of lighting anomalies or partial face occlusion.

### 🎭 Strict Role-Based Access Control (RBAC)
* **Admin Role**: Full system configuration, department management, course/subject catalog, teacher onboarding, student roster oversight, and global system metrics.
* **Teacher Role**: Class timetable scheduling, taking live attendance, single/bulk student face registration, section model retraining, and exportable analytics.
* **Student Role**: Dedicated self-signup portal, personal attendance percentage tracking, subject-wise attendance breakdown, and low attendance warning alerts.

### 📸 Face Enrollment & AI Model Training
* **Interactive Face Capture**: Multi-angle camera capture tool guiding students through face positioning.
* **Bulk Dataset Ingestion**: Upload ZIP archives / CSV spreadsheets containing student photos with automatic serial matching and batch embedding vectorization.
* **Section-Wise Model Training**: On-demand retraining triggers to optimize nearest-neighbor vector indexes for individual classroom sections.

### 📊 Rich Analytics & Automated Alerts
* **Interactive Dashboards**: Interactive charts using Recharts displaying attendance trends, subject performance, and semester-level statistics.
* **Defaulter Identification**: Instantly identifies students falling below institutional attendance thresholds (e.g. 75%).
* **WhatsApp Notification Engine**: Dispatches automated absence alerts directly to parent and teacher phone numbers.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Framework & Core** | [React 18](https://react.dev/), [TypeScript](https://www.typescriptlang.org/), [Vite](https://vitejs.dev/) (SWC compiler) |
| **UI & Styling** | [Tailwind CSS](https://tailwindcss.com/), [shadcn/ui](https://ui.shadcn.com/), [Radix UI](https://www.radix-ui.com/), [Lucide Icons](https://lucide.dev/) |
| **State & Data Fetching** | [@tanstack/react-query](https://tanstack.com/query/latest) (TanStack Query v5), React Context |
| **Animation & UX** | [Framer Motion](https://www.framer.com/motion/), [Sonner](https://sonner.emilkowal.ski/) (Toasts), [Vaul](https://vaul.emilkowal.ski/) |
| **Forms & Validation** | [React Hook Form](https://react-hook-form.com/), [Zod](https://zod.dev/) |
| **Visualization** | [Recharts](https://recharts.org/), [date-fns](https://date-fns.org/) |
| **Backend / BaaS Integration** | [Supabase Client (`@supabase/supabase-js`)](https://supabase.com/docs), FastAPI REST Backend (InsightFace) |
| **Testing & Quality** | [Vitest](https://vitest.dev/), [@testing-library/react](https://testing-library.com/), [Playwright](https://playwright.dev/), [ESLint 9](https://eslint.org/) |

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have the following installed on your machine:
* [Node.js](https://nodejs.org/) (version **18.x** or higher recommended)
* [npm](https://www.npmjs.com/) or [Bun](https://bun.sh/)
* *(Optional)* FastAPI Backend service running on `http://localhost:8000`

### 2. Installation
Navigate to the `attendance_frontend` directory and install project dependencies:

```bash
cd attendance_frontend
npm install
```

### 3. Environment Configuration
Create a `.env` file in the `attendance_frontend` root directory:

```env
# Supabase Configuration
VITE_SUPABASE_URL="https://your-project.supabase.co"
VITE_SUPABASE_PUBLISHABLE_KEY="your-supabase-publishable-key"

# Python AI / Face Recognition Backend URL
VITE_FACE_API_URL="http://localhost:8000"
```

### 4. Run Development Server
Start the local Vite dev server with hot module replacement (HMR):

```bash
npm run dev
```

The application will be live at: **`http://localhost:5173`** (or your designated Vite port).

---

## 🔐 Demo Credentials

Use the pre-configured accounts below for quick local testing:

| Role | Email | Password | Primary Purpose |
| :--- | :--- | :--- | :--- |
| 🛡️ **Admin** | `admin@gmail.com` | `12345678` | Manage Departments, Subjects, Faculty & Global Settings |
| 👨‍🏫 **Teacher** | `tennetiparameshwar@gmail.com` | `12345678` | Conduct Face Attendance, Model Training & Classes |
| 🎓 **Student** | *(Self-Signup via `/signup`)* | — | View Personal Attendance & Profile Statistics |

---

## 🗺️ Application Routes & Role Matrix

| Route | Component | Access Level | Description |
| :--- | :--- | :--- | :--- |
| `/` | `Index.tsx` | Public | Landing / Welcome page |
| `/login` | `Login.tsx` | Public (Unauthenticated) | Role-aware secure login portal |
| `/signup` | `StudentSignup.tsx` | Public (Unauthenticated) | Student onboarding and self-registration |
| `/dashboard` | `Dashboard.tsx` | 🛡️ Admin / 👨‍🏫 Teacher | Main command center & quick actions |
| `/departments` | `Departments.tsx` | 🛡️ Admin only | Academic departments directory & CRUD |
| `/subjects` | `Subjects.tsx` | 🛡️ Admin only | Curriculum and course catalog management |
| `/teachers` | `Teachers.tsx` | 🛡️ Admin only | Faculty management & subject allocation |
| `/students` | `Students.tsx` | 🛡️ Admin / 👨‍🏫 Teacher | Complete student roster with status filters |
| `/register-student` | `RegisterStudent.tsx` | 🛡️ Admin / 👨‍🏫 Teacher | Single student enrollment with face capture |
| `/face-training` | `FaceTraining.tsx` | 👨‍🏫 Teacher only | Live multi-angle student face model training |
| `/bulk-upload` | `BulkUpload.tsx` | 👨‍🏫 Teacher only | Batch ZIP/CSV photo dataset enrollment |
| `/classes` | `Classes.tsx` | 🛡️ Admin / 👨‍🏫 Teacher | Section timetables & classroom schedules |
| `/attendance` | `TakeAttendance.tsx` | 👨‍🏫 Teacher only | AI real-time facial recognition attendance camera |
| `/analytics` | `Analytics.tsx` | 🛡️ Admin / 👨‍🏫 Teacher | Visual attendance metrics, defaulters & reports |
| `/settings` | `Settings.tsx` | 🛡️ Admin only | System configurations, API parameters & thresholds |
| `/student-dashboard` | `StudentDashboard.tsx` | 🎓 Student only | Student portal: attendance %, logs & alerts |

---

## 🏗️ Architecture & Directory Structure

```text
attendance_frontend/
├── public/                 # Static assets & icons
├── src/
│   ├── components/         # Modular React UI components
│   │   ├── layout/         # Header, Sidebar, Dashboard Layouts
│   │   ├── student/        # Student subject mapping & cards
│   │   └── ui/             # Radix + Tailwind primitive components (shadcn)
│   ├── contexts/           # Global React Contexts (AuthContext, etc.)
│   ├── hooks/              # Reusable custom React hooks
│   ├── integrations/       # External service SDKs (Supabase client & schemas)
│   ├── lib/                # Utility helpers & formatting tools (utils.ts)
│   ├── pages/              # Routed view pages (Admin, Teacher, Student)
│   ├── services/           # API communication layer
│   │   ├── faceRecognitionApi.ts  # Face training, crops recognition & WhatsApp API
│   │   ├── notificationService.ts # Real-time alerts & notification dispatch
│   │   └── teacherAdminService.ts # Administration queries & role management
│   ├── test/               # Unit & integration test suites
│   ├── App.tsx             # Root router with RBAC guard wrappers
│   ├── index.css           # Design tokens, CSS variables & glassmorphism styles
│   └── main.tsx            # Application entrypoint & DOM mount
├── .env                    # Local environment variables
├── package.json            # Scripts & project dependencies
├── tailwind.config.ts      # Tailwind design tokens, colors & animations
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite build config & path alias aliases (`@/*`)
└── vitest.config.ts        # Vitest unit test runner config
```

---

## 📜 Available NPM Scripts

| Script | Command | Purpose |
| :--- | :--- | :--- |
| `dev` | `npm run dev` | Runs the local development server at `http://localhost:5173` |
| `build` | `npm run build` | Compiles TypeScript and builds production distribution in `dist/` |
| `build:dev` | `npm run build:dev` | Builds the project using development mode configuration |
| `preview` | `npm run preview` | Locally serves the compiled production build |
| `lint` | `npm run lint` | Runs ESLint 9 across all `.ts`, `.tsx`, and `.js` files |
| `test` | `npm run test` | Executes unit tests with Vitest |
| `test:watch` | `npm run test:watch` | Runs Vitest in interactive watch mode |

---

## 🧪 Testing

### Unit Testing with Vitest
```bash
# Run unit tests once
npm run test

# Run unit tests with file watcher
npm run test:watch
```

### End-to-End Testing with Playwright
```bash
# Run Playwright E2E tests
npx playwright test

# Run Playwright tests with UI mode
npx playwright test --ui
```

---

## 🤝 Contributing

1. **Fork** the repository.
2. Create a feature branch: `git checkout -b feature/amazing-feature`.
3. Commit your changes: `git commit -m "feat: add amazing feature"`.
4. Push to the branch: `git push origin feature/amazing-feature`.
5. Open a **Pull Request**.

---

<div align="center">
  <sub>Built with ❤️ for educational institutions seeking seamless, high-accuracy attendance automation.</sub>
</div>
