import React, { useState } from "react";
import './card.css'

export default function Avis({ deck = [], disabled  }) {
  const [isLoading, setIsLoading] = useState(false);
  const [aiResponse, setAiResponse] = useState(null);
  const [error, setError] = useState(null);
  const [showPopup, setShowPopup] = useState(false);

  const getAvis = async () => {
    if (deck.length === 0) {
        console.log("Aucun deck sélectionné pour l'analyse");
      setError("Aucun deck sélectionné pour l'analyse");
      return;
    }
    else {
        console.log("Analyse du deck en cours...", deck);
    }

    setIsLoading(true);
    setError(null);
    setAiResponse(null);
    setShowPopup(true);

    try {
      // Simulation d'un délai de chargement plus réaliste
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Utiliser directement la réponse simulée
      const simulatedResponse = generateSimulatedAnalysis(deck);
      setAiResponse(simulatedResponse);
    } catch (err) {
      console.error('Erreur lors de l\'analyse:', err);
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

  // Fonction pour générer une analyse simulée
  const generateSimulatedAnalysis = (deckCards) => {
    const analysisTemplates = [
      {
        deck: deck,
        intro: "🎯 Analyse stratégique de votre deck :",
        strengths: ["Bonne synergie défensive", "Coût d'élixir équilibré", "Présence de win conditions solides"],
        weaknesses: ["Vulnérable aux sorts de zone", "Manque de cartes anti-aériennes", "Faible contre les decks de contrôle"],
        suggestions: ["Remplacer une carte par un sort de zone", "Ajouter une défense anti-aérienne", "Considérer une carte de cycle plus rapide"]
      },
      {
        intro: "⚔️ Évaluation tactique de votre composition :",
        strengths: ["Excellent potentiel offensif", "Bonnes cartes de support", "Défenses polyvalentes"],
        weaknesses: ["Coût d'élixir légèrement élevé", "Sensible aux rush rapides", "Manque de flexibilité"],
        suggestions: ["Intégrer une carte de cycle", "Renforcer la défense précoce", "Optimiser l'équilibre élixir"]
      }
    ];

    const randomTemplate = analysisTemplates[Math.floor(Math.random() * analysisTemplates.length)];
    const shuffleArray = (array) => [...array].sort(() => Math.random() - 0.5);

    return `${randomTemplate.intro}

📈 POINTS FORTS :
${shuffleArray(randomTemplate.strengths).slice(0, 2).map(strength => `• ${strength}`).join('\n')}

⚠️ FAIBLESSES POTENTIELLES :
${shuffleArray(randomTemplate.weaknesses).slice(0, 2).map(weakness => `• ${weakness}`).join('\n')}

💡 SUGGESTIONS D'AMÉLIORATION :
${shuffleArray(randomTemplate.suggestions).slice(0, 2).map(suggestion => `• ${suggestion}`).join('\n')}

🏆 Votre deck contient ${deckCards.length} cartes et semble ${Math.random() > 0.5 ? 'bien équilibré' : 'nécessiter quelques ajustements'} pour la méta actuelle.`;
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

      {/* Popup Modal */}
      {showPopup && (
        <div className="fixed inset-0 backdrop-blur-sm bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="relative bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-hidden">
            {/* Bouton de fermeture */}
            <button
              onClick={closePopup}
              className="absolute top-4 right-4 z-10 bg-red-600 hover:bg-red-700 text-white rounded-full w-8 h-8 flex items-center justify-center transition-colors"
            >
              ✕
            </button>

            {/* État de chargement */}
            {isLoading && (
              <div className="flex flex-col items-center justify-center p-12">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-green-600 border-t-transparent mb-4"></div>
                <span className="text-lg text-gray-600">Analyse du deck en cours...</span>
              </div>
            )}

            {/* Affichage des erreurs */}
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

            {/* Affichage de la réponse avec l'image */}
            {aiResponse && !isLoading && (
                // ajout d'une animation d'apparition
              <div className="relative animate-fade-in">
                <img 
                  src="/avis_deck.png" 
                  alt="Analyse du deck"
                  className="w-full h-auto block"
                />
                <div className="deck-analyse-overlay">
                  <div className="deck-analyse-box">
                    <h3>Mousieur voici votre analyse du deck</h3>
                    <div className="deck-analyse-content">
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
