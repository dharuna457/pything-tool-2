import requests

BASE_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/"

def get_word_definition(word):
    url = f"{BASE_URL}{word.lower()}"
    try:
        response = requests.get(url)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        if isinstance(data, dict) and data.get("title") == "No Definitions Found":
            return None # Word not found

        # Extract relevant information
        definitions = []
        for entry in data:
            word_text = entry.get('word')
            phonetic = entry.get('phonetic')

            for meaning in entry.get('meanings', []):
                part_of_speech = meaning.get('partOfSpeech')
                for definition_obj in meaning.get('definitions', []):
                    definition = definition_obj.get('definition')
                    example = definition_obj.get('example')
                    synonyms = definition_obj.get('synonyms')
                    antonyms = definition_obj.get('antonyms')

                    def_entry = {
                        'word': word_text,
                        'phonetic': phonetic,
                        'partOfSpeech': part_of_speech,
                        'definition': definition,
                        'example': example,
                        'synonyms': synonyms,
                        'antonyms': antonyms
                    }
                    definitions.append(def_entry)

        return definitions
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Network error while fetching definition: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred while parsing dictionary data: {e}")

# Example usage
if __name__ == '__main__':
    try:
        word_data = get_word_definition("hello")
        if word_data:
            for entry in word_data:
                print(f"Word: {entry['word']}")
                print(f"  Phonetic: {entry.get('phonetic', 'N/A')}")
                print(f"  Part of Speech: {entry.get('partOfSpeech', 'N/A')}")
                print(f"  Definition: {entry.get('definition', 'N/A')}")
                if entry.get('example'):
                    print(f"    Example: {entry['example']}")
                if entry.get('synonyms'):
                    print(f"    Synonyms: {', '.join(entry['synonyms'])}")
                if entry.get('antonyms'):
                    print(f"    Antonyms: {', '.join(entry['antonyms'])}")
                print("-" * 20)
        else:
            print("Word not found.")

        word_data_fail = get_word_definition("asdfghjkl")
        if not word_data_fail:
            print("Correctly handled 'word not found'.")

    except Exception as e:
        print(f"Test error: {e}")