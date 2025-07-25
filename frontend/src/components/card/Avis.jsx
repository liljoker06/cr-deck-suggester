import React, { useState } from "react";
import axios from "axios";
import './card.css';

export default function Avis({ deck = [], disabled }) {
  const [isLoading, setIsLoading] = useState(false);
  const [aiResponse, setAiResponse] = useState(null);
  const [error, setError] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  const getAvis = async () => {
    if (deck.length !== 8) {
      setError("Le deck doit contenir exactement 8 cartes.");
      return;
    }

    setIsLoading(true);
    setError(null);
    setAiResponse(null);
    setShowPopup(true);

    try {
      const response = await axios.post('http://127.0.0.1:8001/api/analyze-deck-route', {
        deck: deck // On envoie les noms avec espaces, comme tu le veux
      });

      if (response.data && response.data.summary) {
        const summary = response.data.summary;

        const formattedResponse = `
🎯 ${summary.style_de_jeu}

🧪 ${summary.elixir_moyen}
📊 ${summary.popularite_globale}
🔥 ${summary.cartes_populaires}

📋 Détail par carte :
${summary.popularite_cartes.map(item => `• ${item}`).join('\n')}
        `;

        setAiResponse(formattedResponse);
      } else {
        setError("Réponse inattendue de l'analyse.");
      }
    } catch (err) {
      console.error('Erreur API:', err);
      setError("Erreur lors de l'analyse du deck. Veuillez réessayer.");
    } finally {
      setIsLoading(false);
    }
  };

  const closePopup = () => {
    setShowPopup(false);
    setAiResponse(null);
    setError(null);
  };

  return (
    <div className="space-y-4">
      <button
        onClick={getAvis}
        disabled={isLoading || deck.length !== 8}
        className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors duration-200"
      >
        {isLoading ? "Analyse en cours..." : "Avoir un avis sur le Deck"}
      </button>

      {showPopup && (
        <div className="fixed inset-0 backdrop-blur-sm bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="relative bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
            <button
              onClick={closePopup}
              className="absolute top-4 right-4 z-10 bg-red-600 hover:bg-red-700 text-white rounded-full w-8 h-8 flex items-center justify-center transition-colors"
            >
              ✕
            </button>

            {isLoading && (
              <div className="flex flex-col items-center justify-center p-12">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-600 border-t-transparent mb-4"></div>
                <span className="text-lg text-gray-600">Analyse du deck en cours...</span>
              </div>
            )}

            {error && !isLoading && (
              <div className="p-8 text-center">
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                  {error}
                </div>
                <button 
                  onClick={closePopup}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
                >
                  Fermer
                </button>
              </div>
            )}

            {aiResponse && !isLoading && (
              <div className="relative animate-fade-in">
                <img 
                  src="/avis_deck.png" 
                  alt="Analyse du deck"
                  className="w-full h-auto block"
                />
                <div className="deck-analyse-overlay">
                  <div className="deck-analyse-box">
                    <h3>Mousieur voici votre analyse du deck</h3>
                    <div className="deck-analyse-content whitespace-pre-line">
                      {aiResponse}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
