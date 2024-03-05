### Question: What is your understanding of the experiment the team is replicating? What question does it answer? How clear is the team's explanation?

The team seems to want to model opinions on a social media network by using heterogeneity in degree distributions, high values of clustering, and small-world phenomena. There might be a typo, but I don't understand what equal prevalence (0.5 A, 0. B) means (perhaps both 0.5?). I am also not completely understanding what a "group opinion" is in their model. Using small world phenomena as a model, would an opinion be a node? Or some representation of state with the nodes being opinion-skewing content?

### Methodology: Do you understand the methodology? Does it make sense for the question? Are there limitations you see that the team did not address?

I would like to hear more about why the original researchers chose these methods and why this group chooses to replicate these methods. Is one a better ideological fit than others? What were the rationales for the parameters chosen, such as for Wattz-Strogatz graphs with rewiring probabilities of 0, 0.01, and 1? There was a sentence incomplete in that paragraph, so I wasn't sure on all of these details. The personalization methods are well-described, but the sentence introducing them says "...Regardless of method, the user keeps track of the past 20 opinions they were exposed to...". I believe this sentence is misleading as that would imply the most recent 20 are kept track of, when that is only the case for the REC method.

"We then attempted to replicate the “nudge” of the population’s opinion towards A by randomly selecting 10% of a user’s opinions they have seen in the past and replacing them with A. This “nudges” the opinion prevalence towards A by making every active user up to 10% more likely to adopt opinion A." Why?

### Results: Do you understand what the results are (not yet considering their interpretation)? If they are presented graphically, are the visualizations effective? Do all figures have labels on the axes and captions?

The visualizations are somewhat effective. The first shown gives each column its model title, but I believe the titles should be spelled out in full (e.g. WS -> Watts-Strogatz) if there is space. It also needs a title. It's also a little small and not too clear what's happening in the figure. Are we as readers supposed to see any differences in the 1st row? And are we supposed to be unable to see the differences between REC, REF, and OLD in row 2? I think using different colors would (literally) be more illustrative.

Their "figure 2" figure is colorful, which improves upon one of the weaknesses of figure 1. However, the columns lack a corresponding model title. I assume from figure 1 that they are in the same order, but I don't know for sure and I believe they should still be listed here. The axes are also unlabeled. How is evolution measured? Are these also probabilities?

Figure 3 needs a title, but looks good other than that. I'm not sure the A) B) C) D) ordering is needed unless they need to be read in that order; however, I'm guessing they needn't be read in that order based on the other features. The fourth image, called figure 3, needs axes and a legend. If it can be made wider, that would help. I can't tell how many data points there are, but is a line plot like this the best way of respresenting opinion?

Figure 4 part 1 looks good other than the lack of title. I know that P(t) means probability, but maybe add (iterations) after _t_ so that it is clearer what time is measured in. If nudging does the same thing in all cases, is it worth displaying? If what you're trying to capture is the amount of time taken for a nudge to bring a user to decision A, then wouldn't it make more sense to put time on the y-axis? Furthermore, I can't verify that the current x-axis is time. This graph also needs labels.

### Interpretation: Does the draft report interpret the results as an answer to the motivating question? Does the argument hold water?

I see after looking at the paper that the first graph in each section refers to the paper's figure. I stand by my stance on their color choices. The results do look similar, but I don't get much of an argument from the current interpretation section.

### Replication: Are the results in the report consistent with the results from the original paper? If so, how did the authors demonstrate that consistency? Is it quantitative or qualitative?

The results are consistent, and they are demonstrated through visualization. Most of the graphs look very similar to what can be found in the paper.

### Extension: Does the report explain an extension to the original experiment clearly? Can it answer an interesting question that the original experiment did not answer?

I assume the extension is this:
"We potentially seek to use the results of this model to compare to a real world survey result, such as the National Longitudinal Surveys."

I didn't initially register this was the extension and had to go back to find it, so maybe using a label like

```
#### Extension
We potentially seek to use the results of this model to compare to a real world survey result, such as the National Longitudinal Surveys.
```

would be helpful. I don't know what the National Longitudinal Surveys are, but I do think the extension would be cool if the model can verify some result based on survey data.

### Progress: Is the team roughly where they should be at this point, with a replication that is substantially complete and an extension that is clearly defined and either complete or nearly so?

The replication seems to be substantially complete, but the extension does not seem to be.

### Presentation: Is the report written in clear, concise, correct language? Is it consistent with the audience and goals of the report? Does it violate any of the recommendations in my style guideLinks to an external site.?

The report is mostly good, but there is some missing text here and there. I didn't see any huge stylistic red flags.

### Mechanics: Is the report in the right directory with the right file name? Is it formatted professionally in Markdown? Does it include a meaningful title and the full names of the authors? Is the bibliography in an acceptable style?

The report is in the right directory and is in Markdown. It has its authors and title. The annotated bibliography is fine, although could use more explanation for those who don't read the paper.

### Notes:

- More clearly denote sections and subsections in the final report to make it more clear for readers.

- I think when presenting the visualizations, instead of having "figure 3: ..." at the top, it would be more effective to write "figure 3: Opinion of Friends in a Watts-Strogatz network. This graph is really cool because ABC. It was really easy, kinda like 123..." in the Markdown.

- Fine tune the visualizations

- Proofread the report for the various missing text
