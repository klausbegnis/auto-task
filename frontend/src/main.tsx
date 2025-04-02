import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import LandingPage from './components/pages/LandingPage/LandingPage'
import ProjectsPage from './components/ProjectsPage/ProjectsPage'
import './index.css'

const router = createBrowserRouter([
  {
    path: '/',
    element: (
      <>
        <LandingPage />
      </>
    ),
  },
  {
    path: '/projects',
    element: (
      <>
        <ProjectsPage />
      </>
    ),
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
)