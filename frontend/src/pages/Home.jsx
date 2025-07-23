import React from 'react'

export default function Home() {
  return (
    <>
      {/* Hero Section avec thème Clash Royale */}
      <div className="relative isolate px-6  lg:px-8 min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-blue-800">
        
        {/* Effets visuels d'arrière-plan */}
        <div
          aria-hidden="true"
          className="absolute inset-x-0 -top-40 -z-10 transform-gpu overflow-hidden blur-3xl sm:-top-80"
        >
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-[calc(50%-11rem)] aspect-1155/678 w-144.5 -translate-x-1/2 rotate-30 bg-gradient-to-tr from-yellow-400 to-orange-500 opacity-20 sm:left-[calc(50%-30rem)] sm:w-288.75"
          />
        </div>

        {/* Contenu principal */}
        <div className="mx-auto max-w-4xl py-32 sm:py-48 lg:py-56">
          
          {/* Badge d'annonce */}
          <div className="hidden sm:mb-8 sm:flex sm:justify-center">
            <div className="relative rounded-full px-4 py-2 text-sm text-yellow-300 ring-2 ring-yellow-400/30 hover:ring-yellow-400/50 bg-yellow-400/10 backdrop-blur-sm transition-all">
              🏆 Nouvelle saison disponible !{' '}
              <a href="/arenas" className="font-semibold text-yellow-400 hover:text-yellow-300">
                <span aria-hidden="true" className="absolute inset-0" />
                Découvrir <span aria-hidden="true">⚔️</span>
              </a>
            </div>
          </div>

          {/* Titre principal */}
          <div className="text-center">
            <h1 className="text-6xl font-bold tracking-tight text-white sm:text-8xl drop-shadow-2xl">
              CR Deck
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">
                {' '}Suggester
              </span>
            </h1>
            <p className="mt-8 text-xl font-medium text-gray-200 sm:text-2xl max-w-3xl mx-auto leading-relaxed">
              Découvrez les meilleurs decks, analysez les stratégies gagnantes et dominez toutes les arènes de Clash Royale ! 
              <span className="text-yellow-400 font-semibold"> Statistiques en temps réel</span> et conseils d'experts.
            </p>

            {/* Boutons d'action */}
            <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-6">
              <a
                href="/decks"
                className="group relative rounded-lg bg-gradient-to-r from-yellow-500 to-orange-500 px-8 py-4 text-lg font-bold text-white shadow-xl hover:from-yellow-400 hover:to-orange-400 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-yellow-400 transform hover:scale-105 transition-all duration-200"
              >
                <span className="relative z-10">🃏 Explorer les Decks</span>
                <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-yellow-600 to-orange-600 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
              </a>
              
              <a 
                href="/cartes" 
                className="group rounded-lg border-2 border-yellow-400 px-8 py-4 text-lg font-semibold text-yellow-400 hover:bg-yellow-400 hover:text-blue-900 transition-all duration-200 transform hover:scale-105"
              >
                ⚡ Voir les Cartes
              </a>
            </div>

            {/* Stats rapides */}
            <div className="mt-16 grid grid-cols-1 sm:grid-cols-3 gap-8 max-w-2xl mx-auto">
              <div className="text-center p-4 rounded-lg bg-white/10 backdrop-blur-sm border border-white/20">
                <div className="text-3xl font-bold text-yellow-400">107</div>
                <div className="text-sm text-gray-300 mt-1">Cartes disponibles</div>
              </div>
              <div className="text-center p-4 rounded-lg bg-white/10 backdrop-blur-sm border border-white/20">
                <div className="text-3xl font-bold text-yellow-400">17</div>
                <div className="text-sm text-gray-300 mt-1">Arènes différentes</div>
              </div>
              <div className="text-center p-4 rounded-lg bg-white/10 backdrop-blur-sm border border-white/20">
                <div className="text-3xl font-bold text-yellow-400">∞</div>
                <div className="text-sm text-gray-300 mt-1">Combos possibles</div>
              </div>
            </div>
          </div>
        </div>

        {/* Effet visuel bas */}
        <div
          aria-hidden="true"
          className="absolute inset-x-0 top-[calc(100%-13rem)] -z-10 transform-gpu overflow-hidden blur-3xl sm:top-[calc(100%-30rem)]"
        >
          <div
            style={{
              clipPath:
                'polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)',
            }}
            className="relative left-[calc(50%+3rem)] aspect-1155/678 w-144.5 -translate-x-1/2 bg-gradient-to-tr from-purple-500 to-blue-600 opacity-20 sm:left-[calc(50%+36rem)] sm:w-288.75"
          />
        </div>
      </div>

      {/* Section fonctionnalités */}
      <div className="py-24 bg-gray-900">
        <div className="mx-auto max-w-7xl px-6 lg:px-8">
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="text-4xl font-bold tracking-tight text-white sm:text-5xl">
              Pourquoi choisir <span className="text-yellow-400">CR Deck Suggester</span> ?
            </h2>
            <p className="mt-6 text-lg leading-8 text-gray-300">
              Les outils les plus avancés pour analyser et optimiser vos stratégies Clash Royale
            </p>
          </div>
          
          {/* Fonctionnalités */}
          <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
            <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
              
              <div className="flex flex-col items-center text-center p-6 rounded-xl bg-gradient-to-br from-blue-800 to-purple-800 border border-blue-600/30">
                <div className="text-4xl mb-4">📊</div>
                <dt className="text-xl font-semibold leading-7 text-yellow-400">
                  Analyses Avancées
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-300">
                  <p className="flex-auto">
                    Statistiques détaillées de chaque carte, synergies optimales et méta actuel pour dominer vos adversaires.
                  </p>
                </dd>
              </div>

              <div className="flex flex-col items-center text-center p-6 rounded-xl bg-gradient-to-br from-purple-800 to-blue-800 border border-purple-600/30">
                <div className="text-4xl mb-4">🎯</div>
                <dt className="text-xl font-semibold leading-7 text-yellow-400">
                  Decks Personnalisés
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-300">
                  <p className="flex-auto">
                    Suggestions de decks adaptées à votre niveau de trophées et votre arène.
                  </p>
                </dd>
              </div>

              <div className="flex flex-col items-center text-center p-6 rounded-xl bg-gradient-to-br from-blue-800 to-purple-800 border border-blue-600/30">
                <div className="text-4xl mb-4">⚡</div>
                <dt className="text-xl font-semibold leading-7 text-yellow-400">
                  Données Temps Réel
                </dt>
                <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-300">
                  <p className="flex-auto">
                    Informations constamment mises à jour depuis l'API officielle et la communauté des joueurs.
                  </p>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </>
  )
}
