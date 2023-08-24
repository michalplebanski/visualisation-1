import pandas as pd
import matplotlib.pyplot as plt

genres = pd.read_csv('tmdb_genres.csv', header=None, names=['genre_id', 'genres'])
movies = pd.read_csv('tmdb_movies.csv')

# Obliczanie 3. kwartyla liczby głosów
third_quartile = movies['vote_count'].quantile(0.75)

# Filtracja filmów
filtered_movies = movies[movies['vote_count'] > third_quartile]

# Sortowanie filmów według oceny
top_rated_movies = filtered_movies.sort_values(by='vote_average', ascending=False).head(10)

print(top_rated_movies['original_title'])

#GRUPOWANIE PO DACIE

movies['release_date'] = pd.to_datetime(movies['release_date'])

# Filtracja filmów opublikowanych od 2010 do 2016 roku
filtered_movies = movies[(movies['release_date'].dt.year >= 2010) & (movies['release_date'].dt.year <= 2016)]

# Grupowanie i obliczanie średnich
grouped_data = filtered_movies.groupby(filtered_movies['release_date'].dt.year)[['revenue', 'budget']].mean()

def million(x, pos):
    return 'PLN {:2.1f}M'.format(x*1e-6)

formatter = plt.FuncFormatter(million)

fig, axes = plt.subplots()

axes.bar(grouped_data.index, grouped_data['revenue'], color='blue', label='Revenue')
axes.plot(grouped_data.index, grouped_data['budget'], color='red', label='Budget')
axes.set_title('Średni przychód i budżet filmu w latach 2010-2016')
axes.yaxis.set_major_formatter(formatter)

axes.legend(loc=(1.05,0.8))

plt.show()

# Połącz oba dataframe'y na podstawie kolumny 'genre_id'
merged_df = movies.merge(genres, on='genre_id', how='left')

# Eksportuj zmiany do nowego pliku
merged_df.to_csv('merged_movies.csv', index=False)

# Wczytaj dane z pliku CSV
new_data = pd.read_csv('merged_movies.csv')

# Zlicz wystąpienia każdego gatunku
genre_counts = new_data['genres'].value_counts()

# Znajdź gatunek, który pojawia się najczęściej
most_common_genre = genre_counts.idxmax()
most_common_genre_count = genre_counts.max()

print(f"Najczęściej pojawiający się gatunek: {most_common_genre}")
print(f"Liczba filmów tego gatunku: {most_common_genre_count}")

# Filtruj DataFrame, aby pozostały tylko filmy tego gatunku
filtered_df = new_data[new_data['genres'] == longest_avg_runtime_genre]

# Stwórz histogram czasu trwania dla tych filmów
plt.hist(filtered_df['runtime'], bins=20, color='blue', edgecolor='black')
plt.title(f'Histogram czasu trwania filmów gatunku {longest_avg_runtime_genre}')
plt.xlabel('Czas trwania (minuty)')
plt.ylabel('Liczba filmów')
plt.show()
