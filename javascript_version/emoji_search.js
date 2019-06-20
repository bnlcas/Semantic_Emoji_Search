//Functions to search for an emoji

var emoji_mat;
var word_mat;
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "its", "itself", "what", "which", "who", "whom", "this", "that", "these", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "to", "so", "s", "t", "can", "will", "just", "don", "should", "now", "with",]


function InitializeSearch()
{
  //emoji_mat_data
  emoji_mat = math.matrix(emoji_mat_data.data);

  //Load Word Matrix
  word_mat = math.matrix(word_mat_data.data);

  //Load the word dictionary
  //word_dict = JSON.parse(FileReader.readTextFile('word_dict.json'));
  //unicode_rep = JSON.parse(FileReader.readTextFile('unicode_rep.json'));
}

function FindEmoji(search_phrase, n_values = 10)
{
  var search_vector = MakePhraseVec(search_phrase);
  if(search_vector == -1)
  {
      return ['\u{2753}', '\u{1F937}', '\u{2753}'];
  }
  else {
    var similarity = math.multiply(emoji_mat, math.transpose(search_vector));
    var similarity_arr = math.transpose(similarity).toArray()[0];
    var similarity_sorted = similarity_arr.slice(0);
    similarity_sorted.sort(function(a,b){return b-a});

    var suggestions = [];
    for(var i = 0; i < n_values; i++)
    {
      var target_ind = similarity_arr.indexOf(similarity_sorted[i]);
      suggestions.push(unicode_rep[target_ind]);
    }
    return suggestions;
  }
}

function ProcessSearchPhrase(search_phrase)
{
  search_phrase = search_phrase.toLowerCase();
  stop_chars = [':', ';', '-',',', '?', '!']
  for(var i; i < stop_chars.length; i ++)
  {
    search_phrase = search_phrase.replace(stop_chars[i], ' ');
  }

  search_words = search_phrase.split(' ');
  search_words_filtered = [];

  for(var i = 0; i < search_words.length; i ++)
  {
      search_words_filtered.push(search_words[i]);
  }

  return search_words_filtered;
}

function MakePhraseVec(search_phrase)
{
  var processed_words = ProcessSearchPhrase(search_phrase);
  var word_inds = [];
  for(var i = 0; i < processed_words.length; i++)
  {
    try
   {
     var ind = word_dict[processed_words[i]];
     if(typeof ind === 'number')
     {
       word_inds.push(ind);
     }
   }
   catch(e){ }
  }

  if(word_inds.length == 0)
  {
    return -1;
  }
  else {
    var vec_len = word_mat.size()[1];//300
    var phrase_vec = math.subset(word_mat, math.index(word_inds[0], math.range(0, vec_len )));
    for(var i = 1; i < word_inds.length; i++)
    {
      phrase_vec = math.add(phrase_vec, math.subset(word_mat, math.index(word_inds[i], math.range(0, vec_len))));
    }
    var norm = math.sqrt(math.multiply(phrase_vec, math.transpose(phrase_vec)));
    var phrase_vec_norm = math.multiply(phrase_vec, 1.0/norm._data);
    return phrase_vec_norm;
  }
}
