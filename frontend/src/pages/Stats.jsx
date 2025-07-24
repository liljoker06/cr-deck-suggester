import React, { useState, useEffect } from 'react'
import apiService from '../services/apiService'

export default function Stats() {
  const [globalStats, setGlobalStats] = useState(null);
  const [cardsStats, setCardsStats] = useState(null);
  const [playersStats, setPlayersStats] = useState(null);
  const [arenasStats, setArenasStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchAllStats = async () => {
      try {
        setLoading(true);
        const [global, cards, players, arenas] = await Promise.all([
          apiService.getGlobalStats(),
          apiService.request('/stats/cards'),
          apiService.request('/stats/players'),
          apiService.request('/stats/arenas')
        ]);
        
        setGlobalStats(global);
        setCardsStats(cards);
        setPlayersStats(players);
        setArenasStats(arenas);
      } catch (err) {
        setError(err.message);
        console.error('Erreur lors du chargement des statistiques:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAllStats();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement des statistiques...</p>
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
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
      {/* Header */}
      <div className="pt-20 pb-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white sm:text-5xl">
              📊 <span className="text-yellow-400">Statistiques</span> Clash Royale
            </h1>
            <p className="mt-4 text-xl text-gray-300">
              Analyses complètes et métriques détaillées du jeu
            </p>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-12">
        {/* Statistiques globales */}
        {globalStats && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6">📈 Vue d'ensemble</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                <div className="text-4xl font-bold text-yellow-400">{globalStats.totals?.cards || 0}</div>
                <div className="text-gray-300 mt-2">Cartes disponibles</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                <div className="text-4xl font-bold text-blue-400">{globalStats.totals?.arenas || 0}</div>
                <div className="text-gray-300 mt-2">Arènes différentes</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                <div className="text-4xl font-bold text-green-400">{globalStats.totals?.players || 0}</div>
                <div className="text-gray-300 mt-2">Joueurs analysés</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                <div className="text-4xl font-bold text-purple-400">{globalStats.totals?.decks || 0}</div>
                <div className="text-gray-300 mt-2">Decks répertoriés</div>
              </div>
            </div>
          </div>
        )}

        {/* Statistiques des cartes */}
        {cardsStats && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6">🃏 Statistiques des cartes</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Distribution par rareté */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h3 className="text-xl font-bold text-white mb-4">Distribution par rareté</h3>
                <div className="space-y-3">
                  {cardsStats.distribution?.by_rarity && Object.entries(cardsStats.distribution.by_rarity).map(([rarity, count]) => (
                    <div key={rarity} className="flex items-center justify-between">
                      <span className={`px-3 py-1 rounded text-sm font-medium ${
                        rarity === 'Common' ? 'bg-gray-600 text-white' :
                        rarity === 'Rare' ? 'bg-blue-600 text-white' :
                        rarity === 'Epic' ? 'bg-purple-600 text-white' :
                        rarity === 'Legendary' ? 'bg-yellow-600 text-black' :
                        rarity === 'Champion' ? 'bg-red-600 text-white' :
                        'bg-gray-500 text-white'
                      }`}>
                        {rarity}
                      </span>
                      <span className="text-white font-bold">{count}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Distribution par catégorie */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h3 className="text-xl font-bold text-white mb-4">Distribution par catégorie</h3>
                <div className="space-y-3">
                  {cardsStats.distribution?.by_category && Object.entries(cardsStats.distribution.by_category).map(([category, count]) => (
                    <div key={category} className="flex items-center justify-between">
                      <span className="text-gray-300 flex items-center">
                        <span className="mr-2">
                          {category === 'Troop' ? '👥' : 
                           category === 'Spell' ? '⚡' : 
                           category === 'Building' ? '🏰' : '🃏'}
                        </span>
                        {category}
                      </span>
                      <span className="text-white font-bold">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Cartes avec évolution */}
            <div className="mt-6 bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white">Cartes avec évolution</h3>
                  <p className="text-gray-400">Cartes pouvant être évoluées</p>
                </div>
                <div className="text-3xl font-bold text-green-400">
                  {cardsStats.cards_with_evolution || 0}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Statistiques des joueurs */}
        {playersStats && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6">👥 Statistiques des joueurs</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Top joueurs */}
              {playersStats.top_players && playersStats.top_players.length > 0 && (
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                  <h3 className="text-xl font-bold text-white mb-4">🏆 Top Joueurs</h3>
                  <div className="space-y-3">
                    {playersStats.top_players.map((player, index) => (
                      <div key={index} className="flex items-center justify-between bg-gray-800/50 rounded-lg p-3">
                        <div>
                          <div className="text-white font-bold">{player.name}</div>
                          <div className="text-gray-400 text-sm">
                            Niveau {player.level} • {player.clan || 'Sans clan'}
                          </div>
                        </div>
                        <div className="text-yellow-400 font-bold">
                          {player.trophies?.toLocaleString()} 🏆
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Distribution par pays */}
              {playersStats.distribution?.by_country && (
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                  <h3 className="text-xl font-bold text-white mb-4">🌍 Top Pays</h3>
                  <div className="space-y-2">
                    {Object.entries(playersStats.distribution.by_country).slice(0, 8).map(([country, count]) => (
                      <div key={country} className="flex items-center justify-between">
                        <span className="text-gray-300">{country}</span>
                        <span className="text-white font-bold">{count}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Statistiques générales des joueurs */}
            {playersStats.general && (
              <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                  <div className="text-3xl font-bold text-yellow-400">
                    {playersStats.general.avg_trophies?.toFixed(0) || 0}
                  </div>
                  <div className="text-gray-300 mt-2">Trophées moyens</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                  <div className="text-3xl font-bold text-blue-400">
                    {playersStats.general.avg_level?.toFixed(1) || 0}
                  </div>
                  <div className="text-gray-300 mt-2">Niveau moyen</div>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 text-center">
                  <div className="text-3xl font-bold text-green-400">
                    {((playersStats.general.players_with_clan / playersStats.general.total_players) * 100).toFixed(1) || 0}%
                  </div>
                  <div className="text-gray-300 mt-2">Joueurs en clan</div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Statistiques des arènes */}
        {arenasStats && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6">🏛️ Statistiques des arènes</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Distribution par paliers de trophées */}
              {arenasStats.distribution_by_trophy_range && (
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                  <h3 className="text-xl font-bold text-white mb-4">Distribution par trophées</h3>
                  <div className="space-y-3">
                    {Object.entries(arenasStats.distribution_by_trophy_range).map(([range, count]) => (
                      <div key={range} className="flex items-center justify-between">
                        <span className="text-gray-300">{range} trophées</span>
                        <span className="text-white font-bold">{count} arènes</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Informations générales */}
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h3 className="text-xl font-bold text-white mb-4">Informations générales</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">Arènes totales:</span>
                    <span className="text-white font-bold">{arenasStats.total_arenas}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">Trophées minimum:</span>
                    <span className="text-yellow-400 font-bold">{arenasStats.trophy_range?.min} 🏆</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-300">Trophées maximum:</span>
                    <span className="text-yellow-400 font-bold">{arenasStats.trophy_range?.max}+ 🏆</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
