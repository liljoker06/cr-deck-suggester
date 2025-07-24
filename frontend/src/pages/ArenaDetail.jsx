import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useArenas } from '../hooks/useApi';
import Arenas from '../components/card/Arenas';

export default function ArenaDetail() {
  const { arenaNumber } = useParams();
  const navigate = useNavigate();
  const { arenas, loading, error } = useArenas();

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement de l'arène...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-400 text-6xl mb-4">⚠️</div>
          <h2 className="text-white text-2xl mb-2">Erreur de chargement</h2>
          <p className="text-gray-300">{error}</p>
          <button 
            onClick={() => navigate('/arenas')}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Retour aux arènes
          </button>
        </div>
      </div>
    );
  }

  // Trouver l'arène correspondante
  const arena = arenas.find(a => a.number === parseInt(arenaNumber));

  if (!arena) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="text-yellow-400 text-6xl mb-4">🏛️</div>
          <h2 className="text-white text-2xl mb-2">Arène non trouvée</h2>
          <p className="text-gray-300">L'arène #{arenaNumber} n'existe pas</p>
          <button 
            onClick={() => navigate('/arenas')}
            className="mt-4 bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition-colors"
          >
            Retour aux arènes
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
      {/* Bouton retour */}
      <div className="pt-20 pb-4">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <button 
            onClick={() => navigate('/arenas')}
            className="flex items-center text-yellow-400 hover:text-yellow-300 transition-colors mb-6"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Retour aux arènes
          </button>
        </div>
      </div>

      {/* Composant Arenas avec l'arène spécifique */}
      <Arenas arena={arena} />
    </div>
  );
}
