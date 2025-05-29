// src/App.jsx
import { useState } from 'react';
import { format, fromUnixTime } from 'date-fns';
import { ru } from 'date-fns/locale';
import './App.css';

function App() {
  const [city, setCity] = useState('');
  const [weatherData, setWeather] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const formatDate = (timestampInSeconds) => {
    const date = fromUnixTime(timestampInSeconds);

    return format(date, 'HH:mm, EEEE', {
      locale: ru
    });
  };

  const formatPressure = (pressure) => {
    return pressure / 1000;
  };

  const handleSearch = async () => {
    if (!city.trim()) {
      setError('Введите название города');
      return;
    }
    try {
      setError('');
      const response = await fetch('http://localhost:8000/weather', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ city: city })
      });
      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Ошибка запроса');
      }
      const data = await response.json();
      setWeather(data);
    } catch (err) {
      setError(err.message);
      setWeather(null);
    }
  };

  // Обработчик клавиш
  const handleKeyUp = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="container">
      <h1>Прогноз погоды</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Введите город и нажмите Enter"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          onKeyUp={handleKeyUp}
          className="search-input"
        />
        {isLoading && <p className="loading">Загрузка...</p>}
        {error && <p className="error">{error}</p>}
      </div>

      {weatherData && (
        <div className="weather-container">
          <div className="current-weather">
            <div className="weather-header">
              <h2>
                {weatherData.hourly_forecast[0].city}, {weatherData.hourly_forecast[0].country}
              </h2>
              <div className="current-time">
                {formatDate(weatherData.hourly_forecast[0].time)}
              </div>
            </div>

            <div className="weather-grid">
              <div className="weather-item">
                <span>🌡️ Температура:</span>
                {weatherData.hourly_forecast[0].current_temp} °C
              </div>
              <div className="weather-item">
                <span>💨 Ветер:</span>
                {weatherData.hourly_forecast[0].wind_speed} м/с
              </div>
              <div className="weather-item">
                <span>💧 Влажность:</span>
                {weatherData.hourly_forecast[0].humidity}%
              </div>
              <div className="weather-item">
                <span>📌 Давление:</span>
                {formatPressure(weatherData.hourly_forecast[0].pressure)} атм
              </div>
              <div className="weather-item full-width">
                <span>🌤️ Состояние:</span>
                {weatherData.hourly_forecast[0].description}
              </div>
            </div>
          </div>

          <div className="hourly-forecast">
            <h3>Прогноз на следующие часы:</h3>
            <div className="forecast-list">
              {weatherData.hourly_forecast.slice(1).map((item, index) => (
                <div key={`forecast-${index}`} className="forecast-card">
                  <div className="forecast-time">
                    {formatDate(item.time)}
                  </div>
                  <div className="forecast-grid">
                    <div className="forecast-item">
                      <span>🌡️</span>
                      {item.current_temp} °C
                    </div>
                    <div className="forecast-item">
                      <span>💨</span>
                      {item.wind_speed} м/с
                    </div>
                    <div className="forecast-item">
                      <span>💧</span>
                      {item.humidity}%
                    </div>
                    <div className="forecast-item">
                      <span>📌</span>
                      {formatPressure(item.pressure)} атм
                    </div>
                    <div className="forecast-description">
                      {item.description}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
