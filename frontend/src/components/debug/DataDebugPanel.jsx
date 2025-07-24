import React, { useState } from 'react';
import { useGlobalStats } from '../../hooks/useApi';
import apiService from '../../services/apiService';

export default function DataDebugPanel() {
  const { stats, loading, error, refetch } = useGlobalStats();
  const [updating, setUpdating] = useState(false);
  const [updateMessage, setUpdateMessage] = useState('');

  const handleUpdateData = async () => {
    try {
      setUpdating(true);
      setUpdateMessage('Mise à jour en cours...');
      
      await apiService.updateData();
      
      setUpdateMessage('✅ Données mises à jour avec succès !');
      setTimeout(() => {
        refetch();
        setUpdateMessage('');
      }, 2000);
      
    } catch (err) {
      setUpdateMessage(`❌ Erreur lors de la mise à jour: ${err.message}`);
      setTimeout(() => setUpdateMessage(''), 5000);
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="fixed bottom-4 right-4 bg-gray-800 text-white p-4 rounded-lg shadow-lg">
        <div className="animate-pulse">Chargement des statistiques...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="fixed bottom-4 right-4 bg-red-800 text-white p-4 rounded-lg shadow-lg max-w-sm">
        <div className="font-bold">Erreur de connexion</div>
        <div className="text-sm mt-1">
          Vérifiez que le serveur backend fonctionne sur le port 8000
        </div>
        <div className="text-xs mt-2 opacity-75">{error}</div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-4 right-4 bg-gray-800 text-white p-4 rounded-lg shadow-lg max-w-sm">
      <div className="font-bold text-yellow-400 mb-3">📊 Statistiques DB</div>
      
      <div className="text-sm space-y-2 mb-4">
        <div className="flex justify-between items-center">
          <span>🃏 Cartes:</span>
          <span className="font-bold text-green-400">{stats?.totals?.cards || stats?.total_cards || 0}</span>
        </div>
        <div className="flex justify-between items-center">
          <span>🏰 Arènes:</span>
          <span className="font-bold text-blue-400">{stats?.totals?.arenas || stats?.total_arenas || stats?.arenas?.total || 0}</span>
        </div>
        <div className="flex justify-between items-center">
          <span>👥 Joueurs:</span>
          <span className="font-bold text-purple-400">{stats?.totals?.players || stats?.players?.total || stats?.total_players || 0}</span>
        </div>
      </div>

      <button
        onClick={handleUpdateData}
        disabled={updating}
        className={`w-full text-xs py-2 px-3 rounded ${
          updating 
            ? 'bg-gray-600 cursor-not-allowed' 
            : 'bg-blue-600 hover:bg-blue-700'
        } transition-colors`}
      >
        {updating ? '🔄 Mise à jour...' : '🔄 Mettre à jour les données'}
      </button>

      {updateMessage && (
        <div className="text-xs mt-2 p-2 bg-gray-700 rounded">
          {updateMessage}
        </div>
      )}
    </div>
  );
}
