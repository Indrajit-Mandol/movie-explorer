import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import HomePage from "./pages/HomePage";
import MoviesPage from "./pages/MoviesPage";
import MovieDetailPage from "./pages/MovieDetailPage";
import ActorsPage from "./pages/ActorsPage";
import ActorProfilePage from "./pages/ActorProfilePage";
import DirectorsPage from "./pages/DirectorsPage";
import DirectorProfilePage from "./pages/DirectorProfilePage";
import FavoritesPage from "./pages/FavoritesPage";

export default function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/movies" element={<MoviesPage />} />
        <Route path="/movies/:id" element={<MovieDetailPage />} />
        <Route path="/actors" element={<ActorsPage />} />
        <Route path="/actors/:id" element={<ActorProfilePage />} />
        <Route path="/directors" element={<DirectorsPage />} />
        <Route path="/directors/:id" element={<DirectorProfilePage />} />
        <Route path="/favorites" element={<FavoritesPage />} />
        {/* Catch-all redirect to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  );
}
