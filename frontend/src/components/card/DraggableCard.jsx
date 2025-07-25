import React, { useState, useEffect, useRef } from 'react';

export default function DraggableCard({ card, isInDeck = false, onAddToDeck }) {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);

  // Fermer le menu si on clique à l'extérieur
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowMenu(false);
      }
    };

    if (showMenu) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => {
        document.removeEventListener('mousedown', handleClickOutside);
      };
    }
  }, [showMenu]);

  const handleDragStart = (e) => {
    const cardData = {
      name: card.name,
      category: card.category,
      elixir_cost: card.elixir_cost,
      image: card.image,
      description: card.description,
      hitpoints: card.hitpoints,
      damage: card.damage,
      dps: card.dps,
      hit_speed: card.hit_speed,
      range: card.range,
      count: card.count,
      special_damage: card.special_damage,
      evolution: card.evolution,
      evolution_image: card.evolution_image,
      evolution_ids: card.evolution_ids
    };
    
    e.dataTransfer.setData('text/plain', JSON.stringify(cardData));
    e.dataTransfer.effectAllowed = 'copy';
  };

  const handleMenuClick = (e) => {
    e.stopPropagation();
    setShowMenu(!showMenu);
  };

  const handleAddClick = (e) => {
    e.stopPropagation();
    if (onAddToDeck) {
      onAddToDeck();
    }
    setShowMenu(false);
  };

  return (
    <div
      draggable={!isInDeck}
      onDragStart={!isInDeck ? handleDragStart : undefined}
      className={`
        relative bg-white/10 backdrop-blur-sm rounded-lg border border-white/20 p-4 transition-all duration-200 group
        ${!isInDeck 
          ? 'hover:bg-white/20 transform hover:scale-105 cursor-grab active:cursor-grabbing' 
          : 'opacity-50 cursor-not-allowed'
        }
        ${isInDeck ? 'ring-2 ring-yellow-400' : ''}
      `}
      title={isInDeck ? 'Cette carte est déjà dans votre deck' : 'Glissez cette carte dans votre deck ou utilisez le menu'}
    >
      {/* Menu avec 3 petits points - Visible au hover ou si la carte est dans le deck */}
      <div className={`absolute top-2 right-2 ${isInDeck ? 'block' : 'opacity-0 group-hover:opacity-100'} transition-opacity duration-200`}>
        {isInDeck ? (
          <div className="bg-yellow-400 text-black rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">
            ✓
          </div>
        ) : (
          <div className="relative" ref={menuRef}>
            <button
              onClick={handleMenuClick}
              className="bg-gray-700 hover:bg-gray-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs transition-colors duration-200"
              title="Options"
            >
              ⋯
            </button>
            
            {/* Menu déroulant */}
            {showMenu && (
              <div className="absolute top-8 right-0 bg-gray-800 border border-gray-600 rounded-md shadow-lg z-20 min-w-32">
                <button
                  onClick={handleAddClick}
                  className="w-full px-3 py-2 text-left text-white hover:bg-gray-700 transition-colors duration-200 rounded-md text-sm"
                >
                  ➕ Ajouter au deck
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Image de la carte */}
      <div className="aspect-square rounded-lg mb-3 flex items-center justify-center relative">
        {card.className="bg-gradient-to-r from-blue-900 via-purple-900 to-blue-800" ? (
            <img
            src={card.image}
            alt={card.name}
            className="w-64 h-64 object-contain"
            referrerPolicy="no-referrer"
            onError={() => console.log("Image échouée")}
            />
        ) : null}
        <div className="text-4xl" style={{ display: card.image ? 'none' : 'block' }}>
          {card.category === 'Troop' ? '👥' : 
           card.category === 'Spell' ? '⚡' : 
           card.category === 'Building' ? '🏰' : '🃏'}
        </div>
      </div>
      
      {/* Informations de la carte */}
      <div className="text-center">
        <h3 className="text-white font-bold text-sm mb-1 truncate" title={card.name}>
          {card.name}
        </h3>
        
        <div className="flex justify-between items-center text-xs mb-2">
         
          {card.elixir_cost && (
            <span className="bg-purple-600 text-white px-2 py-1 rounded text-xs font-medium flex items-center gap-1">
              {card.elixir_cost}
              <img 
                src="/elixir.png" 
                alt="Élixir" 
                className="w-3 h-3 inline-block"
              />
            </span>
          )}
        </div>
        
        <div className="text-gray-400 text-xs">
          {card.category || 'Catégorie inconnue'}
        </div>
        
        {card.evolution_ids && card.evolution_ids.length > 0 && (
          <div className="mt-2">
            <span className="bg-green-600 text-white px-2 py-1 rounded text-xs font-medium">
              🔄 Évolution
            </span>
          </div>
        )}
      </div>
    </div>
  );
}
