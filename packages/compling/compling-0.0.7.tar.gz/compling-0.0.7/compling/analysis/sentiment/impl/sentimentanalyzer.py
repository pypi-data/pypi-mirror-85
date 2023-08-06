import re
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from compling.analysis.sentiment.lexicon.lexicon import Lexicon
from compling.analysis.sentiment.sentiment import SentimentLexiconBased
from typing import *
from wordcloud import WordCloud


class SentimentAnalyzer(SentimentLexiconBased):
    """
    The most popular unsupervised strategies used in sentiment analysis are lexical-based methods. They make use of a predefined list of words, where each word is associated with a specific sentiment. Lexicon-based strategies are very efficient and simple methods. They make use of a sentiment lexicon to assign a polarity value to each text document by following a basic algrithm. A sentiment lexicon is a list of lexical features (e.g., words, phrase, etc.) which are labeled according to their semantic orientation (i.e. polarity) as either positive or negative.

    A SentimentAnalyzer object allows to perform sentiment analysis through a lexicon-based approach.

    SentimentAnalyzer uses a summation _strategy_: the polarity level of a document is calculated as the sum of the polarities of all the words making up the
    document.

    The analysis detects negation pattern and reverses the negated tokens polarity.

    Providing a regex, you can filter sentences/paragraphs/documents to analyze.

    Providing a pos list and/or a dep list you can filter the words whose polarities will be summed.
    """

    def __init__(self, tokens: Iterable[dict],
                 group_by_field: str, id_index_field: str = None, date_field: str = None,
                 token_field: str = "text",
                 pos: Tuple[str, ...] = ('VERB', 'NOUN'), dep: Tuple[str, ...] = None) -> None:
        """
        **\_\_init\_\_**: Creates a new SentimentAnalyzer object.

        Args:
            tokens (Iterable[dict]): Stream of token records produced during the tokenization stage.
            token_field (str, optional, default=text): A field containing the text of tokens (e.g. text, lemma, ...). <br/> The tokens will be grouped by this field.
            group_by_field (Union[str, List[str]]): Fields linked to tokens in the corpus (e.g. doc_id, sent_id, metadata1, ...).  <br/> The tokens will be grouped by these field.
            id_index_field (str, optional, default=None): Id field for record in a index produced during tokenization stage. If None, it will be ignored and you won't be able to filter any sentence, paragraph, document by a regex.

                    Valid input values:
                    ["doc_id", "para_id", "sent_id"]

            date_field (str, optional, default=None): The field containing a date that refers to vectors (e.g. could be a 'publication_date' metadata). <br/> If not None, the data will be sorted by date_value.
            pos (str, optional, default=VERB,NOUN): Part of speech of the tokens. <br/> Filters the most informative tokens: tokens whose PoS tag is in the 'pos' list. <br/> If None, the filter will be ignored.
            dep (Tuple[str, ...], optional, default=None): Dependencies of the tokens. <br/> Filters the most informative tokens: tokens whose dep tag is in the 'dep' list. <br/> If None, the filter will be ignored.
        """

        self.token_field = token_field + '_'

        if isinstance(group_by_field, str):
            self.group_by_field = [group_by_field + '_']
        else:
            self.group_by_field = [g + '_' for g in group_by_field]

        self.group_by_field_key = " + ".join(self.group_by_field)

        self.date_field = date_field if date_field is None else date_field + '_'

        self.id_index_field = id_index_field

        if id_index_field is not None:
            self.id_index_field += "_"
            self.index = defaultdict(lambda: defaultdict(list))
        else:
            self.index = defaultdict(list)

        for record in tokens:
            # filter tokens
            if pos is not None and len(pos) > 0 and record['pos_'] not in pos: continue
            if dep is not None and len(dep) > 0 and record['dep_'] not in dep: continue

            # inversion polarity
            token = record[self.token_field]
            if record['is_negated_']:
                token = 'NOT_' + token

            key = " + ".join([record[g] for g in self.group_by_field])

            if self.id_index_field is not None:
                self.index[key][record[self.id_index_field]].append(token)
            else:
                self.index[key].append(token)

    def filter(self, index: Iterable[dict], regex_pattern: str) -> None:
        """
        Filters the sentences/paragraphs/documents to be considered to calculate a polarity value.

        Args:
            index (Iterable[dict]): Records of an index produced during the tokenization stage (e.g. sentences, paragraphs, documents).
            regex_pattern (str): The filter uses this regex.
        """

        if self.id_index_field is None:
            print("You can't filter sentences/paragraphs/documents because you hadn't set id_index_field during the instance creation.")
            print("All sentences/paragraphs/documents are considered.")
            return

        pattern = re.compile(regex_pattern)

        # Index filtered grouped by group_by_field
        new_index = defaultdict(list)
        for record in index:
            if pattern.match(record[self.token_field]):
                key = " + ".join([record[g] for g in self.group_by_field])
                new_index[key].extend(self.index[key][record[self.id_index_field]])
        self.index = new_index


    def run(self, lexicon: Lexicon, tf_: bool = True) -> Tuple[dict, dict]:
        """
        Performs sentiment analysis of the texts in the index calculating the polarity level for each different
        group_by_field value.

        Args:
            lexicon (Lexicon): a Lexicon object.
            tf_ (bool, optional, default=True): If True, considers the frequency of the words: the token polarity will be summed n times, where n is the token frequency in the text. <br/> If false, the polarity of a token in the text will be summed exactly once. <br/>

        Returns:
            Tuple[dict, dict]: Two dict are returned:

                * the first contains the polarity value for each different grouped_by_field value.

                     Example:
                     {
                      "grouped_by_field1": {
                                            "pos": 0,
                                            "neg":1,
                                            "obj":3},
                       ...,
                     }

                * the second contains the words classified as positive/negative with their polarity value for each different grouped_by_field value.

                     Example:
                     {
                      "grouped_by_field1": {
                                            "neg": {
                                                    "fuck": 12.0,
                                                    "bad": 7.0,
                                                    ...
                                                    },
                                            "pos": {
                                                    "good": 11.0,
                                                    "love": 2.0,
                                                    ...
                                                    }
                                            },
                      ...
                    }
        """

        # Info about sentiment
        polarities = defaultdict(lambda: defaultdict(int))

        # sentiment words dict
        words = defaultdict(lambda: {'pos': defaultdict(int), 'neg': defaultdict(int)})

        for group_by_field_key in tqdm(self.index, desc='Sentiment Analysis in progress ...', position=0, leave=True):
            bag_of_word = self.index[group_by_field_key]
            tokens_polarities = lexicon.polarities(bag_of_word)

            for token, sentiment in tokens_polarities.items():
                for polarity, value in sentiment.items():
                    polarities[group_by_field_key][polarity] += value

                if sentiment['pos'] > sentiment['neg']:
                    old = words[group_by_field_key]['pos']['token']
                    words[group_by_field_key]['pos'].update(
                        {token: sentiment['pos'] + old if tf_ else sentiment['pos']})

                elif sentiment['neg'] > sentiment['pos']:
                    old = words[group_by_field_key]['neg']['token']
                    words[group_by_field_key]['neg'].update(
                        {token: sentiment['neg'] + old if tf_ else old})

        self.polarities = polarities
        self.words = words
        return polarities, words

    def plot(self, ylabel: str = None, xlabel: str = None, figsize: Tuple[int, int] = (12, 8),
             title: str = None, hidexticks: bool = True, save: bool = None) -> None:
        """
        Draws a scatter plot of positive and negative polarities level for each group_by_field sort by time (If date_field is not None).

        Args:
            xlabel (str, optional, default=None): Label on x-axis.
            ylabel (str, optional, default=None): Label on y-axis.
            figsize (Tuple[int, int], optional, default=12,8): Figure size: width, height in inches.
            title (str, optional, default=None): If not None, draws title string on the figure.
            hidexticks (bool, optional, default=False): If True, hides xticks.
            save (str, optional, default=None): Figure is not saved if save is None. <br/> Set it with an output name if you want save it.
        """

        plt.figure(figsize=figsize)
        plt.plot()

        polarities = {"pos": {"color": "r", "label": "Positive (+)"},
                      "neg": {"color": "b", "label": "Negative (-)"}}

        for polarity in polarities:
            plt.tight_layout()
            x, y = list(self.polarities.keys()), [self.polarities[id_vector][polarity] for id_vector in self.polarities]
            plt.plot(x, y, label=polarities[polarity]["label"], color=polarities[polarity]["color"])
            plt.xticks(x, rotation="horizontal")
            plt.title('\n{}'.format(title), size=20)
            if not ylabel is None:
                plt.ylabel('{}\n'.format(ylabel), size=20)
            if not xlabel is None:
                plt.xlabel('\n{}'.format(xlabel), size=20)

        plt.legend()  # bbox_to_anchor=(1.5, 0.5), loc='right', ncol=1)

        if not hidexticks:
            plt.xticks([])

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

    def circleplot(self, radius: int = 3, figsize: Tuple[int, int] = (10, 10), title: str = None,
                   width_modifier: float = 1.3,
                   offset: float = 0.8, save: bool = False) -> None:
        """
        Draws a circle plot of positive and negative polarities level for each group_by_field sort by time (If date_field is not None).

        Args:
            radius (int, optional, default=3): The radius of the circle.
            figsize (Tuple[int, int], optional, default=10,10): Figure size: width, height in inches.
            width_modifier (float, optional, default=1.3): Width of the bars.
            offset (float, optional, default=0.8): Offset for the label on the bars.
            save (str, optional, default=None): Figure is not saved if save is None. <br/> Set it with an output name if you want save it.
            title (str, optional, default=None):  If not None, draws title string on the figure.
        """

        data = self.polarities

        plt.figure(figsize=figsize)
        ax = plt.subplot(111, polar=True)
        ax.axis('off')

        N = len(data)
        radius = radius

        theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
        width = (width_modifier * np.pi) / N

        pos_values, neg_values = np.array([data[i]["pos"] for i in data]), np.array([data[i]["neg"] for i in data])

        pos = ax.bar(theta, pos_values, width=width, bottom=radius)
        neg = ax.bar(theta, -neg_values, width=width, bottom=radius)

        for p, n in zip(pos, neg):
            p.set_facecolor("red")
            p.set_alpha(0.8)
            n.set_facecolor("black")
            n.set_alpha(0.8)

        # labeling
        for i, bar in enumerate(pos):
            t = theta[i] + 0.002
            x, y = (bar.get_x() + width / 2, offset * len(list(data)[i]) + bar.get_height())
            if np.cos(t) < 0: t = t - np.pi
            ax.text(x, y, list(data)[i], rotation=np.rad2deg(t), ha="center", va="center")

        if title:
            plt.title(title)

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

    def wordcloud(self, grouped_by_field_value: Union[str, List[str]],
                  polarity: str,
                  color: str = 'black', title: str = None, figsize: Tuple[int, int] = (10, 8),
                  save=None, width: int = 1000, height: int = 1000,
                  max_words: int = 100) -> None:
        """
        Draws a word Cloud with the words of grouped_by_field_value.

        Args:
            grouped_by_field_value (Union[str, List[str]]): Value for the group_by_fields.
            polarity (str): Positive or negative polarity.

                    Valid input:
                    ["pos", "neg"]

            color (str, optional, default=black): Background color.
            title (str, optional, default=None): If not None, draws title string on the figure.
            figsize (Tuple[int, int], optional, default=10,10): Figure size: width, height in inches.
            save (str, optional, default=None): Figure is not saved if save is None. Set it with a output name if you want save it.
            width (int, optional, default=1000): Width of the canvas.
            height (int, optional, default=1000): Height of the canvas.
            max_words (int, optional, default=100): The maximum number of words.
        """

        if not isinstance(self.group_by_field, str):
            grouped_by_field_value = " + ".join(grouped_by_field_value)

        sentiment = self.words[grouped_by_field_value][polarity]
        wordcloud = WordCloud(width=width, background_color=color, height=height,
                              max_words=max_words).generate_from_frequencies(sentiment)
        plt.figure(figsize=figsize)
        plt.imshow(wordcloud, label=title)
        plt.title(title, fontsize=22)

        if save:
            plt.tight_layout()
            fig1 = plt.gcf()
            plt.show()
            plt.draw()
            fig1.savefig(save)
        else:
            plt.show()

        plt.close()
