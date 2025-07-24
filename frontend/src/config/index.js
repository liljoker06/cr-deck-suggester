// Configuration de l'application
export const config = {
  // URL de l'API backend
  apiBaseUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  
  // Configuration par défaut pour les requêtes
  defaultTimeout: 10000,
  
  // Paramètres de pagination
  defaultPageSize: 20,
  maxPageSize: 100,
  
  // Messages d'erreur
  errorMessages: {
    networkError: 'Erreur de connexion. Vérifiez que le serveur backend est démarré.',
    serverError: 'Erreur serveur. Veuillez réessayer plus tard.',
    notFound: 'Ressource non trouvée.',
    invalidRequest: 'Requête invalide.'
  }
};

// Environnement de développement
export const isDevelopment = import.meta.env.MODE === 'development';

// Debug
export const showDebugPanel = isDevelopment;
