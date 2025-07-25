import React, { useState } from 'react';

export default function CardDecks({ deckCards, onCardDrop, onCardRemove }) {
  const [dragOverSlot, setDragOverSlot] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDragEnter = (e, slotIndex) => {
    e.preventDefault();
    setDragOverSlot(slotIndex);
  };

  const handleDragLeave = (e) => {
    setTimeout(() => {
      setDragOverSlot(null);
    }, 50);
  };

  const handleDrop = (e, slotIndex) => {
    e.preventDefault();
    setDragOverSlot(null);
    
    try {
      const dragData = e.dataTransfer.getData('text/plain');
      
      if (!dragData) {
        return;
      }
      
      const cardData = JSON.parse(dragData);
      onCardDrop(cardData, slotIndex);
    } catch (error) {
      console.error('Erreur lors du drop de la carte:', error);
    }
  };

  const handleRemoveCard = (slotIndex) => {
    onCardRemove(slotIndex);
  };

  const renderCardSlot = (card, index) => {
    const isEmpty = !card;
    const isDragOver = dragOverSlot === index;
    
    return (
      <div
        key={index}
        className={`
          relative aspect-square rounded-lg border-2 border-dashed transition-all duration-200
          ${isEmpty 
            ? `border-gray-600 bg-gray-800/50 hover:border-yellow-400 hover:bg-gray-700/50 ${isDragOver ? 'border-yellow-400 bg-yellow-400/20 scale-105' : ''}` 
            : 'border-yellow-400 bg-gradient-to-br from-blue-900/80 to-purple-900/80'
          }
        `}
        onDragOver={handleDragOver}
        onDragEnter={(e) => handleDragEnter(e, index)}
        onDragLeave={handleDragLeave}
        onDrop={(e) => handleDrop(e, index)}
        style={{ minHeight: '120px' }}
      >
        {isEmpty ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-4xl text-gray-600 mb-2">+</div>
              <p className="text-xs text-gray-500">Glissez une carte ici</p>
            </div>
          </div>
        ) : (
          <div className="relative h-full p-2">
            {/* Bouton de suppression */}
            <button
              onClick={() => handleRemoveCard(index)}
              className="absolute top-1 right-1 bg-red-600 hover:bg-red-700 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs z-10 transition-colors duration-200"
              title="Retirer la carte"
            >
              ×
            </button>
            
            {/* Image de la carte */}
            <div className="w-full h-2/3 rounded mb-2 flex items-center justify-center">
              {card.image ? (
                <img
                  src={card.image}
                  alt={card.name}
                  className="w-48 h-48 object-contain"
                  onError={(e) => {
                    e.target.style.display = 'none';
                    e.target.nextSibling.style.display = 'block';
                  }}
                />
              ) : null}
              <div className="text-2xl" style={{ display: card.image ? 'none' : 'block' }}>
                {card.category === 'Troop' ? '👥' : 
                 card.category === 'Spell' ? '  ' : 
                 card.category === 'Building' ? '🏰' : '🃏'}
              </div>
            </div>
            
            {/* Informations de la carte */}
            <div className="text-center">
              <h4 className="text-white text-xs font-medium truncate mb-1" title={card.name}>
                {card.name}
              </h4>
              <div className="flex justify-center items-center gap-1">
                {card.elixir_cost && (
                  <span className="bg-purple-600 text-white px-1 py-0.5 rounded text-xs">
                    {card.elixir_cost}
                    <img 
                      src="/elixir.png" 
                      alt="Élixir" 
                      className="w-3 h-3 inline-block"
                    />
                  </span>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    );
  };

  // deux rangées de 4
  const topRowCards = deckCards.slice(0, 4);
  const bottomRowCards = deckCards.slice(4, 8);

    const validCards = deckCards
    .filter(card => card && card.elixir_cost)
    .map(card => {
        const parsed = parseFloat(card.elixir_cost);
        return isNaN(parsed) ? null : parsed;
    })
    .filter(cost => cost !== null);

    const totalElixirCost = validCards.reduce((sum, cost) => sum + cost, 0);

    const averageElixirCost = validCards.length > 0
    ? (totalElixirCost / validCards.length).toFixed(1)
    : "0.0";


  return (
    <div className="bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-6">
      {/* En-tête du deck */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2">Votre Deck</h2>
        <p className="text-gray-300 text-sm mb-3">
          Glissez-déposez des cartes ou utilisez les menus ⋯ pour créer votre deck parfait
        </p>
        <div className="flex items-center gap-4 text-sm">
          <span className="text-gray-300">
            Cartes: <span className="text-yellow-400 font-bold">
              {deckCards.filter(card => card).length}/8
            </span>
          </span>
          <span className="text-gray-300">
            Coût moyen: <span className="text-purple-400 font-bold">
              {averageElixirCost}
              <img 
                src="/elixir.png" 
                alt="Élixir" 
                className="w-3 h-3 inline-block"
              />
            </span>
          </span>
          <span className="text-gray-300">
            Coût total: <span className="text-blue-400 font-bold">
              {totalElixirCost}
              <img 
                src="/elixir.png" 
                alt="Élixir" 
                className="w-3 h-3 inline-block"
              />
            </span>
          </span>
        </div>
      </div>

      {/* Grille du deck */}
      <div className="space-y-4">
        {/* Première rangée */}
        <div className="grid grid-cols-4 gap-4">
          {topRowCards.map((card, index) => renderCardSlot(card, index))}
        </div>
        
        {/* Deuxième rangée */}
        <div className="grid grid-cols-4 gap-4">
          {bottomRowCards.map((card, index) => renderCardSlot(card, index + 4))}
        </div>
      </div>

      {/* Indicateur de progression */}
      <div className="mt-4">
        <div className="w-full bg-gray-700 rounded-full h-2">
          <div 
            className="bg-gradient-to-r from-yellow-400 to-yellow-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(deckCards.filter(card => card).length / 8) * 100}%` }}
          ></div>
        </div>
        <p className="text-center text-gray-400 text-xs mt-1">
          {deckCards.filter(card => card).length === 8 
            ? "Deck complet ! 🎉" 
            : `Il vous manque ${8 - deckCards.filter(card => card).length} carte(s)`
          }
        </p>
      </div>
    </div>
  );
}
