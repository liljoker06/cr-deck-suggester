import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Arenas({ arena }) {
  const navigate = useNavigate();
  if (!arena) {
    return (
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🏛️</div>
          <h3 className="text-white text-xl mb-2">Aucune arène sélectionnée</h3>
          <p className="text-gray-400">Veuillez sélectionner une arène à afficher</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
      {/* En-tête de l'arène */}
      <div className="text-center mb-8">
        <div className="flex items-center justify-center space-x-4 mb-4">
          <div className="w-16 h-16 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-2xl">
            {arena.number}
          </div>
          <div>
            <h1 className="text-4xl font-bold text-white sm:text-5xl">
              {arena.name}
            </h1>
            <p className="text-xl text-gray-300 mt-2">
              Arène {arena.number} • {arena.min_trophies.toLocaleString()} 🏆
            </p>
          </div>
        </div>
      </div>

      {/* Image principale de l'arène */}
      <div className="mb-8">
        <div className="aspect-video bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 flex items-center justify-center overflow-hidden">
          {arena.image ? (
            <img
              src={arena.image}
              alt={arena.name}
              referrerPolicy="no-referrer"
              onError={() => console.log("Image échouée")}
              className="w-full h-full object-contain"
            />
          ) : null}
          <div 
            className="text-8xl text-gray-600 flex items-center justify-center w-full h-full" 
            style={{ display: arena.image ? 'none' : 'flex' }}
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
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Numéro d'arène:</span>
              <span className="text-yellow-400 font-bold">#{arena.number}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-gray-400">Trophées requis:</span>
              <span className="text-yellow-400 font-bold">
                {arena.min_trophies.toLocaleString()} 🏆
              </span>
            </div>
            {arena.chest_reward_multiplier && (
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Multiplicateur coffres:</span>
                <span className="text-green-400 font-bold">
                  x{arena.chest_reward_multiplier}
                </span>
              </div>
            )}
            {arena.shop_chest_reward_multiplier && (
              <div className="flex items-center justify-between">
                <span className="text-gray-400">Multiplicateur boutique:</span>
                <span className="text-blue-400 font-bold">
                  x{arena.shop_chest_reward_multiplier}
                </span>
              </div>
            )}
          </div>
        </div>

        {/* Niveau de difficulté */}
        <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-3">🎯</span>
            Difficulté
          </h3>
          <div className="text-center">
            <div className={`inline-block px-6 py-3 rounded-full text-lg font-bold mb-4 ${
              arena.min_trophies < 1000 ? 'bg-green-600 text-white' :
              arena.min_trophies < 3000 ? 'bg-yellow-600 text-black' :
              arena.min_trophies < 5000 ? 'bg-orange-600 text-white' :
              'bg-red-600 text-white'
            }`}>
              {arena.min_trophies < 1000 ? '🟢 Débutant' :
               arena.min_trophies < 3000 ? '🟡 Intermédiaire' :
               arena.min_trophies < 5000 ? '🟠 Avancé' :
               '🔴 Expert'}
            </div>
            <p className="text-gray-400 text-sm">
              {arena.min_trophies < 1000 ? 'Parfait pour commencer votre aventure' :
               arena.min_trophies < 3000 ? 'Niveau modéré, stratégie requise' :
               arena.min_trophies < 5000 ? 'Niveau élevé, maîtrise nécessaire' :
               'Niveau maximum, pour les meilleurs joueurs'}
            </p>
          </div>
        </div>
      </div>

      {/* Conseils pour l'arène */}
      <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6 mb-8">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center">
          <span className="text-2xl mr-3">💡</span>
          Conseils pour cette arène
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="text-gray-300">
            <h4 className="font-semibold text-white mb-2">Stratégies recommandées:</h4>
            <ul className="space-y-1 text-sm">
              {arena.min_trophies < 1000 ? (
                <>
                  <li>• Apprenez les bases du jeu</li>
                  <li>• Utilisez des decks simples</li>
                  <li>• Concentrez-vous sur l'économie d'élixir</li>
                </>
              ) : arena.min_trophies < 3000 ? (
                <>
                  <li>• Développez votre sens tactique</li>
                  <li>• Maîtrisez les cycles de cartes</li>
                  <li>• Apprenez les combinaisons de base</li>
                </>
              ) : arena.min_trophies < 5000 ? (
                <>
                  <li>• Perfectionnez vos micro-gestions</li>
                  <li>• Maîtrisez les contre-attaques</li>
                  <li>• Adaptez-vous aux méta actuels</li>
                </>
              ) : (
                <>
                  <li>• Excellence dans tous les domaines</li>
                  <li>• Anticipation des mouvements adverses</li>
                  <li>• Maîtrise parfaite du timing</li>
                </>
              )}
            </ul>
          </div>
          <div className="text-gray-300">
            <h4 className="font-semibold text-white mb-2">Points clés:</h4>
            <ul className="space-y-1 text-sm">
              <li>• Gérez bien votre élixir</li>
              <li>• Observez les patterns adverses</li>
              <li>• Protégez vos tours</li>
              <li>• Soyez patient dans vos attaques</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Progression */}
      {arena.number < 24 && (
        <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <span className="text-2xl mr-3">🚀</span>
            Prochaine étape
          </h3>
          <div className="text-center">
            <p className="text-gray-300 mb-4">
              Continuez à jouer pour atteindre l'arène suivante !
            </p>
            <button 
              onClick={() => navigate(`/arena/${arena.number + 1}`)}
              className="bg-gradient-to-r from-yellow-400 to-orange-500 text-black px-6 py-2 rounded-full font-bold hover:from-yellow-500 hover:to-orange-600 transition-all duration-200 transform hover:scale-105"
            >
              Arène {arena.number + 1} →
            </button>
          </div>
        </div>
      )}
    </div>
    
  );
}


