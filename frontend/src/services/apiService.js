import { config } from '../config';

const API_BASE_URL = config.apiBaseUrl;

class ApiService {
  async request(endpoint, options = {}) {
    try {
      const url = `${API_BASE_URL}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Erreur API (${endpoint}):`, error);
      throw error;
    }
  }

  // Statistiques globales
  async getGlobalStats() {
    return this.request('/stats');
  }

  // Cartes
  async getAllCards(filters = {}) {
    const params = new URLSearchParams();
    if (filters.category) params.append('category', filters.category);
    if (filters.rarity) params.append('rarity', filters.rarity);
    if (filters.limit) params.append('limit', filters.limit);

    const queryString = params.toString();
    return this.request(`/cards${queryString ? `?${queryString}` : ''}`);
  }

  async getCardByName(cardName) {
    return this.request(`/cards/${encodeURIComponent(cardName)}`);
  }

  async getCardsStats() {
    return this.request('/cards/stats/count');
  }

  // Arènes
  async getAllArenas() {
    return this.request('/arenas');
  }

  async getArenaByNumber(arenaNumber) {
    return this.request(`/arenas/${arenaNumber}`);
  }

  async getArenasStats() {
    return this.request('/arenas/stats/count');
  }

  // Decks
  async getAllDecks(filters = {}) {
    const params = new URLSearchParams();
    if (filters.arena_number) params.append('arena_number', filters.arena_number);
    if (filters.limit) params.append('limit', filters.limit);

    const queryString = params.toString();
    return this.request(`/decks${queryString ? `?${queryString}` : ''}`);
  }

  async getDeckById(deckId) {
    return this.request(`/decks/${deckId}`);
  }

  async getDecksStats() {
    return this.request('/decks/stats/count');
  }

  // Mise à jour des données
  async updateData() {
    return this.request('/update-data');
  }
}

// Export d'une instance singleton
export default new ApiService();
