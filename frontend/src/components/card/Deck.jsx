import React, { useState } from 'react';
import { useCards } from '../../hooks/useApi';
import CardDecks from './CardDecks';
import DraggableCard from './DraggableCard';
// import FilterBar from './FilterBar';

export default function Deck() {
  // etat pour stocker les 8 cartes du deck (vides)
  const [deckCards, setDeckCards] = useState(new Array(8).fill(null));
  
  const [filters, setFilters] = useState({
    category: '',
    elixir_cost: '',
    has_evolution: '',
    limit: 50
  });

  // récupérer les cartes
  const { cards, loading, error } = useCards(filters);

  // drag & drop
  const handleCardDrop = (card, slotIndex) => {
    const isCardInDeck = deckCards.some(deckCard => deckCard && deckCard.name === card.name);
    
    if (isCardInDeck) {
      alert('Cette carte est déjà dans votre deck !');
      return;
    }

    // ajout de la carte à l'emplacement spécifié
    const newDeckCards = [...deckCards];
    newDeckCards[slotIndex] = card;
    setDeckCards(newDeckCards);
  };

  // suppression d'une carte du deck
  const handleCardRemove = (slotIndex) => {
    const newDeckCards = [...deckCards];
    newDeckCards[slotIndex] = null;
    setDeckCards(newDeckCards);
  };

  // ajout d'une carte via le menu (alternative au drag & drop)
  const handleAddCardToDeck = (card) => {
    const isCardInDeck = deckCards.some(deckCard => deckCard && deckCard.name === card.name);
    if (isCardInDeck) {
      return;
    }

    const emptySlotIndex = deckCards.findIndex(deckCard => deckCard === null);
    if (emptySlotIndex === -1) {
      return;
    }

    const newDeckCards = [...deckCards];
    newDeckCards[emptySlotIndex] = card;
    setDeckCards(newDeckCards);
    
  };

  // Gestion des filtres
  const handleFilterChange = (filterName, value) => {
    setFilters(prev => ({
      ...prev,
      [filterName]: value
    }));
  };

  const resetFilters = () => {
    setFilters({
      category: '',
      elixir_cost: '',
      has_evolution: '',
      limit: 50
    });
  };

  // sauvegarder le deck
  const saveDeck = () => {
    const completeDeck = deckCards.filter(card => card !== null);
    if (completeDeck.length !== 8) {
      alert('Votre deck doit contenir exactement 8 cartes !');
      return;
    }
    console.log('Deck à sauvegarder:', completeDeck.map(card => card.name));
    alert('Deck sauvegardé avec succès ! 🎉');
  };

  // réinitialiser le deck
  const resetDeck = () => {
    if (window.confirm('Êtes-vous sûr de vouloir vider votre deck ?')) {
      setDeckCards(new Array(8).fill(null));
    }
  };

  // cartes déjà dans le deck
  const getCardsInDeck = () => {
    return deckCards.filter(card => card !== null).map(card => card.name);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-400 mx-auto"></div>
          <p className="text-white mt-4 text-xl">Chargement des cartes...</p>
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
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800 pt-16">
      {/* En-tête */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Section du deck */}
        <div className="mb-12">
          <CardDecks 
            deckCards={deckCards}
            onCardDrop={handleCardDrop}
            onCardRemove={handleCardRemove}
          />
          
          {/* Boutons d'action */}
          <div className="mt-6 flex gap-4 justify-center">
            <button
              onClick={saveDeck}
              disabled={deckCards.filter(card => card).length !== 8}
              className="px-6 py-3 bg-green-600 hover:bg-green-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors duration-200"
            >
              Sauvegarder le Deck (console.log)
            </button>
            <button
              onClick={resetDeck}
              className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors duration-200"
            >
              Vider le Deck
            </button>
          </div>
        </div>

        {/* Section des cartes disponibles */}
        <div>

          {/* Grille des cartes */}
          <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-white">Cartes disponibles</h2>
              <div className="text-gray-300 text-sm">
                Glissez les cartes ou utilisez les menus ⋯ pour les ajouter
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {cards.length === 0 ? (
                <div className="col-span-full text-center py-12">
                  <div className="text-6xl mb-4">🔍</div>
                  <h3 className="text-white text-xl mb-2">Aucune carte trouvée</h3>
                  <p className="text-gray-400">Essayez de modifier vos filtres</p>
                </div>
              ) : (
                cards.map((card, index) => (
                  <DraggableCard
                    key={card.name || index}
                    card={card}
                    isInDeck={getCardsInDeck().includes(card.name)}
                    onAddToDeck={() => handleAddCardToDeck(card)}
                  />
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
