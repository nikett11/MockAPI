document.addEventListener('DOMContentLoaded', () => {
    // --- DOM Element References ---
    const tweetsContainer = document.getElementById('tweets-container');
    const newsContainer = document.getElementById('news-container');
    const usersContainer = document.getElementById('users-container');
    const weatherContainer = document.getElementById('weather-container');
    const eventsContainer = document.getElementById('events-container');

    const tweetsTabBtn = document.getElementById('tweets-tab');
    const newsTabBtn = document.getElementById('news-tab');
    const usersTabBtn = document.getElementById('users-tab');
    const weatherTabBtn = document.getElementById('weather-tab');
    const eventsTabBtn = document.getElementById('events-tab');

    const newsDetailModalElement = document.getElementById('newsDetailModal');
    const userDetailModalElement = document.getElementById('userDetailModal');
    const weatherDetailModalElement = document.getElementById('weatherDetailModal');

    let newsDetailModal;
    let userDetailModal;
    let weatherDetailModal;

    // Mapping for weather descriptions to icon filenames
    const weatherIconMap = {
        "Moderate rain": "moderate_rain.png",
        "Overcast clouds": "overcast_clouds.png",
        "Light drizzle": "drizzly.png",
        "Partly cloudy": "partly_cloudy.png",
        "Intermittent rain": "intermittent_rain.png",
        "Heavy rain": "heavy_rain.png",
        "Cloudy with occasional rain": "cloudy.png",
        "Scattered thunderstorms": "scattered_thunderstorms.png",
        "Light rain showers": "light_rain_showers.png",
        "Drizzly": "drizzly.png",
        // Add more mappings as needed based on your descriptions and icons
    };

    // Initialize the Bootstrap Modals if the elements exist
    if (newsDetailModalElement) {
        newsDetailModal = new bootstrap.Modal(newsDetailModalElement);
    }
    if (userDetailModalElement) {
        userDetailModal = new bootstrap.Modal(userDetailModalElement);
    }
    if (weatherDetailModalElement) {
        weatherDetailModal = new bootstrap.Modal(weatherDetailModalElement);
    }

    // --- Data Fetching Functions ---

    /**
     * Fetches a single user by ID and displays their details in a modal.
     * @param {string} userId - The ID of the user to fetch.
     */
    const fetchUserById = async (userId) => {
        try {
            const response = await fetch(`/mock-users/${userId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const user = await response.json();

            if (userDetailModal) {
                document.getElementById('modal-user-profile-image').src = user.profile_image_url || 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png';
                document.getElementById('modal-user-name').textContent = user.name || 'N/A';
                document.getElementById('modal-user-username').textContent = `@${user.username || 'N/A'}`;
                document.getElementById('modal-user-description').textContent = user.description || 'No description available.';
                document.getElementById('modal-user-created-at').textContent = `Joined: ${new Date(user.created_at).toLocaleDateString()}`;
                document.getElementById('modal-user-protected').textContent = `Protected: ${user.protected ? 'Yes' : 'No'}`;
                document.getElementById('modal-user-verified').textContent = `Verified: ${user.verified ? 'Yes' : 'No'}`;

                const userUrlElement = document.getElementById('modal-user-url');
                if (user.url) {
                    userUrlElement.href = user.url;
                    userUrlElement.style.display = 'inline-block';
                } else {
                    userUrlElement.style.display = 'none';
                }
                userDetailModal.show();
            }
        } catch (error) {
            console.error(`Error fetching user ${userId}:`, error);
            alert('Failed to load user details.');
        }
    };

    /**
     * Fetches tweets from the API and renders them in the UI.
     */
    const fetchTweets = async () => {
        try {
            const response = await fetch('/mock-tweets');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            tweetsContainer.innerHTML = ''; // Clear previous content
            if (data && data.length > 0) {
                data.forEach(tweet => {
                    const tweetElement = document.createElement('div');
                    tweetElement.classList.add('list-group-item', 'list-group-item-action');

                    const usernameSpan = document.createElement('span');
                    usernameSpan.classList.add('username-link'); // Add a class for styling
                    usernameSpan.textContent = `@${tweet.username || 'N/A'}`;
                    usernameSpan.style.cursor = 'pointer'; // Indicate clickability
                    usernameSpan.style.color = '#007bff'; // Bootstrap primary color
                    usernameSpan.style.textDecoration = 'underline';

                    usernameSpan.addEventListener('click', (event) => {
                        event.stopPropagation(); // Prevent tweet item click from firing
                        fetchUserById(tweet.author_id); // Use author_id to fetch user details
                    });

                    const headerDiv = document.createElement('div');
                    headerDiv.classList.add('d-flex', 'w-100', 'justify-content-between');
                    const h5 = document.createElement('h5');
                    h5.classList.add('mb-1');
                    h5.appendChild(usernameSpan);
                    headerDiv.appendChild(h5);

                    const smallDate = document.createElement('small');
                    smallDate.textContent = new Date(tweet.created_at).toLocaleString();
                    headerDiv.appendChild(smallDate);

                    const pText = document.createElement('p');
                    pText.classList.add('mb-1');
                    pText.textContent = tweet.text;

                    const metricsDiv = document.createElement('div');
                    metricsDiv.classList.add('d-flex', 'justify-content-around', 'mt-2');
                    metricsDiv.innerHTML = `
                        <small>Likes: ${tweet.public_metrics ? tweet.public_metrics.like_count : 0}</small>
                        <small>Retweets: ${tweet.public_metrics ? tweet.public_metrics.retweet_count : 0}</small>
                        <small>Replies: ${tweet.public_metrics ? tweet.public_metrics.reply_count : 0}</small>
                        <small>Quotes: ${tweet.public_metrics ? tweet.public_metrics.quote_count : 0}</small>
                    `;

                    tweetElement.appendChild(headerDiv);
                    tweetElement.appendChild(pText);
                    tweetElement.appendChild(metricsDiv);

                    tweetsContainer.appendChild(tweetElement);
                });
            } else {
                tweetsContainer.innerHTML = '<p class="text-muted">No tweets available.</p>';
            }
        } catch (error) {
            console.error('Error fetching tweets:', error);
            tweetsContainer.innerHTML = '<p class="text-danger">Failed to load tweets.</p>';
        }
    };

    /**
     * Fetches news articles from the API and renders them in the UI.
     */
    const fetchNews = async () => {
        try {
            const response = await fetch('/mock-news');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            newsContainer.innerHTML = ''; // Clear previous content
            if (data && data.length > 0) {
                data.forEach(newsItem => {
                    const newsElement = document.createElement('div');
                    newsElement.classList.add('list-group-item', 'list-group-item-action', 'news-item-card');
                    
                    newsElement.innerHTML = `
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">${newsItem.title}</h5>
                            <small>${new Date(newsItem.publishedAt).toLocaleString()}</small>
                        </div>
                        <p class="mb-1">${newsItem.description}</p>
                        <small>Source: ${newsItem.source?.name || 'N/A'}</small>
                    `;

                    // Add click event listener to show the modal with details
                    newsElement.addEventListener('click', () => {
                        if (newsDetailModal) {
                            document.getElementById('modal-news-title').textContent = newsItem.title || '';
                            document.getElementById('modal-news-source-author').textContent = `Source: ${newsItem.source?.name || 'N/A'} | Published: ${new Date(newsItem.publishedAt).toLocaleString()}`;
                            document.getElementById('modal-news-content').textContent = newsItem.content || newsItem.description || '';
                            document.getElementById('modal-news-url').href = newsItem.url || '#';

                            const modalImage = document.getElementById('modal-news-image');
                            if (newsItem.urlToImage) {
                                modalImage.src = newsItem.urlToImage;
                                modalImage.style.display = 'block';
                            } else {
                                modalImage.style.display = 'none';
                            }
                            newsDetailModal.show();
                        }
                    });
                    newsContainer.appendChild(newsElement);
                });
            } else {
                newsContainer.innerHTML = '<p class="text-muted">No news available.</p>';
            }
        } catch (error) {
            console.error('Error fetching news:', error);
            newsContainer.innerHTML = '<p class="text-danger">Failed to load news.</p>';
        }
    };

    /**
     * Fetches users from the API and renders them in the UI.
     */
    const fetchUsers = async () => {
        try {
            const response = await fetch('/mock-users');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            usersContainer.innerHTML = ''; // Clear previous content
            if (data && data.length > 0) {
                data.forEach(user => {
                    const userElement = document.createElement('div');
                    userElement.classList.add('list-group-item', 'list-group-item-action', 'user-item-card');
                    
                    userElement.innerHTML = `
                        <div class="d-flex w-100 justify-content-between align-items-center">
                            <img src="${user.profile_image_url || 'https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png'}" class="rounded-circle me-3" alt="Profile Image" width="50" height="50">
                            <div>
                                <h5 class="mb-1">${user.name || 'N/A'}</h5>
                                <small>@${user.username || 'N/A'}</small>
                            </div>
                        </div>
                        <p class="mb-1 mt-2">${user.description || 'No description available.'}</p>
                    `;

                    userElement.addEventListener('click', () => {
                        fetchUserById(user.id);
                    });
                    usersContainer.appendChild(userElement);
                });
            } else {
                usersContainer.innerHTML = '<p class="text-muted">No users available.</p>';
            }
        } catch (error) {
            console.error('Error fetching users:', error);
            usersContainer.innerHTML = '<p class="text-danger">Failed to load users.</p>';
        }
    };

    /**
     * Fetches weather data from the API and renders them in the UI.
     */
    const fetchWeather = async () => {
        try {
            const response = await fetch('/mock-weather');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            weatherContainer.innerHTML = ''; // Clear previous content
            if (data && data.length > 0) {
                data.forEach(weatherItem => {
                    const weatherElement = document.createElement('div');
                    weatherElement.classList.add('list-group-item', 'list-group-item-action', 'weather-item-card');
                    
                    weatherElement.innerHTML = `
                        <div class="d-flex w-100 justify-content-between align-items-center">
                            <img src="/static/weather_icons/${weatherIconMap[weatherItem.description] || ''}" alt="Weather Icon" width="40" height="40" class="me-3">
                            <div class="weather-info-text">
                                <h5 class="mb-1">${weatherItem.location.area || 'N/A'}</h5>
                                <small>${weatherItem.description || 'N/A'}</small>
                            </div>
                            <span class="badge bg-primary rounded-pill">${weatherItem.temperature}°C</span>
                        </div>
                    `;

                    weatherElement.addEventListener('click', () => {
                        if (weatherDetailModal) {
                            document.getElementById('modal-weather-area').textContent = weatherItem.location.area || 'N/A';
                            document.getElementById('modal-weather-icon').src = `/static/weather_icons/${weatherIconMap[weatherItem.description] || ''}`;
                            document.getElementById('modal-weather-description').textContent = weatherItem.description || 'N/A';
                            document.getElementById('modal-weather-temperature').textContent = `${weatherItem.temperature}°C`;

                            const forecastContainer = document.getElementById('modal-weather-forecast');
                            forecastContainer.innerHTML = '';
                            if (weatherItem.forecast && weatherItem.forecast.length > 0) {
                                weatherItem.forecast.forEach(forecast => {
                                    const forecastDiv = document.createElement('div');
                                    forecastDiv.classList.add('text-center');
                                    forecastDiv.innerHTML = `
                                        <h6>${forecast.day}</h6>
                                        <p>${forecast.condition}</p>
                                        <p>${forecast.temp_min}°C - ${forecast.temp_max}°C</p>
                                    `;
                                    forecastContainer.appendChild(forecastDiv);
                                });
                            }
                            weatherDetailModal.show();
                        }
                    });
                    weatherContainer.appendChild(weatherElement);
                });
            } else {
                weatherContainer.innerHTML = '<p class="text-muted">No weather data available.</p>';
            }
        } catch (error) {
            console.error('Error fetching weather:', error);
            weatherContainer.innerHTML = '<p class="text-danger">Failed to load weather data.</p>';
        }
    };

    /**
     * Fetches events data from the API and renders them in the UI.
     */
    const fetchEvents = async () => {
        try {
            const response = await fetch('/mock-events');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            eventsContainer.innerHTML = ''; // Clear previous content
            if (data && data.length > 0) {
                data.forEach(eventItem => {
                    const eventElement = document.createElement('div');
                    eventElement.classList.add('list-group-item', 'list-group-item-action', 'event-item-card');
                    
                    const startDate = new Date(eventItem.start_date).toLocaleString();
                    let endDate = 'N/A';
                    if (eventItem.end_date) {
                        endDate = new Date(eventItem.end_date).toLocaleString();
                    }

                    eventElement.innerHTML = `
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">${eventItem.name || 'N/A'}</h5>
                            <small>${startDate} - ${endDate}</small>
                        </div>
                        <p class="mb-1">Location: ${eventItem.location.address || 'N/A'}, ${eventItem.location.city || 'N/A'}</p>
                    `;

                    eventsContainer.appendChild(eventElement);
                });
            } else {
                eventsContainer.innerHTML = '<p class="text-muted">No events available.</p>';
            }
        } catch (error) {
            console.error('Error fetching events:', error);
            eventsContainer.innerHTML = '<p class="text-danger">Failed to load events.</p>';
        }
    };

    // --- Event Listeners ---

    // Add event listeners for tab changes to fetch data
    if (tweetsTabBtn) {
        tweetsTabBtn.addEventListener('shown.bs.tab', fetchTweets);
    }
    if (newsTabBtn) {
        newsTabBtn.addEventListener('shown.bs.tab', fetchNews);
    }
    if (usersTabBtn) {
        usersTabBtn.addEventListener('shown.bs.tab', fetchUsers);
    }
    if (weatherTabBtn) {
        weatherTabBtn.addEventListener('shown.bs.tab', fetchWeather);
    }
    if (eventsTabBtn) {
        eventsTabBtn.addEventListener('shown.bs.tab', fetchEvents);
    }

    // --- Initial Fetch ---
    // Fetch tweets by default since it's the first active tab
    fetchTweets();
});