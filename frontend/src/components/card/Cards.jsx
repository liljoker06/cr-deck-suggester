import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Cards({ card }) {
  const navigate = useNavigate();
  if (!card) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🏛️</div>
          <h3 className="text-white text-xl mb-2">Aucune carte sélectionnée</h3>
          <p className="text-gray-400">Veuillez sélectionner une carte à afficher</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      {/* En-tête de l'carte */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center space-x-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-2xl">
            {card.number}
          </div>
          <div>
            <h1 className="text-4xl font-bold text-white sm:text-5xl">
              {card.name}
            </h1>
            <p className="text-xl text-gray-300 mt-2">
              Carte {card.number} • {card.min_trophies.toLocaleString()} 🏆
            </p>
          </div>
        </div>
      </div>

      {/* Image principale de la carte */}
      <div className="mb-8">
        <div className="aspect-video bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 flex items-center justify-center overflow-hidden">
          {card.image ? (
            <img
              src={card.image}
              alt={card.name}
              referrerPolicy="no-referrer"
              onError={() => console.log("Image échouée")}
              className="w-full h-full object-contain"
            />
          ) : null}
          <div 
            className="text-8xl text-gray-600 flex items-center justify-center w-full h-full" 
            style={{ display: card.image ? 'none' : 'flex' }}
          >
            🏛️
          </div>
        </div>
      </div>

      {/* Informations détaillées */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        {/* Statistiques principales */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-3">📊</span>
            Statistiques
          </h3>
        </div>

        {/* Niveau de difficulté */}

      </div>

      {/* Progression */}
      {card.number < 190 && (
        <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-3">🚀</span>
            Prochaine carte
          </h3>
          <div className="text-center">
            <p className="text-gray-300 mb-4">
              Prochaine carte !
            </p>
            <button 
              onClick={() => navigate(`/card/${card.number + 1}`)}
              className="bg-gradient-to-r from-yellow-400 to-orange-500 text-black px-6 py-2 rounded-full font-bold hover:from-yellow-500 hover:to-orange-600 transition-all duration-200 transform hover:scale-105"
            >
              Carte {card.number + 1} →
            </button>
          </div>
        </div>
      )}
    </div>
    
  );
}


