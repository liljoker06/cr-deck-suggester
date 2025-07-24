import { useState, useEffect } from 'react';
import apiService from '../services/apiService';

export const useGlobalStats = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await apiService.getGlobalStats();
        setStats(data);
      } catch (err) {
        setError(err.message);
        console.error('Erreur lors du chargement des statistiques:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  const refetch = async () => {
    await fetchStats();
  };

  return { stats, loading, error, refetch };
};

export const useCards = (filters = {}) => {
  const [cards, setCards] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCards = async () => {
      try {
        setLoading(true);
        const data = await apiService.getAllCards(filters);
        setCards(data);
      } catch (err) {
        setError(err.message);
        console.error('Erreur lors du chargement des cartes:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchCards();
  }, [JSON.stringify(filters)]);

  return { cards, loading, error };
};

export const useArenas = () => {
  const [arenas, setArenas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArenas = async () => {
      try {
        setLoading(true);
        const data = await apiService.getAllArenas();
        setArenas(data);
      } catch (err) {
        setError(err.message);
        console.error('Erreur lors du chargement des arènes:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchArenas();
  }, []);

  return { arenas, loading, error };
};

export const useArena = (arenaNumber) => {
  const [arena, setArena] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchArena = async () => {
      if (!arenaNumber) {
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const data = await apiService.getArenaByNumber(arenaNumber);
        setArena(data);
      } catch (err) {
        setError(err.message);
        console.error('Erreur lors du chargement de l\'arène:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchArena();
  }, [arenaNumber]);

  return { arena, loading, error };
};

export const useDecks = (filters = {}) => {
  const [decks, setDecks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDecks = async () => {
      try {
        setLoading(true);
        const data = await apiService.getAllDecks(filters);
        setDecks(data);
      } catch (err) {
        setError(err.message);
        console.error('Erreur lors du chargement des decks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDecks();
  }, [JSON.stringify(filters)]);

  return { decks, loading, error };
};
