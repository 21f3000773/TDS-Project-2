## Data Analysis and Insights Report

### Summary Statistics

The dataset analyzed includes information from 2,363 entries, encompassing various metrics across 165 unique countries. Below are the key summary statistics:

1. **Country Distribution**:
   - The dataset features a diverse array of countries, with Argentina being the most frequently represented country in the dataset (18 occurrences).

2. **Temporal Coverage**:
   - The data spans from 2005 to 2023, with an average year of 2014.76.
   - There is a standard deviation of 5.06 years, indicating a relatively even spread across the observed years.

3. **Life Ladder (Subjective Well-Being)**:
   - The average Life Ladder score is 5.48, indicating moderate levels of well-being among respondents.
   - The score ranges from 1.281 to 8.019, suggesting significant variability in well-being perceptions across countries.

4. **Log GDP per Capita**:
   - The mean log GDP per capita is approximately 9.40, indicating a general correlation with economic prosperity.
   - The GDP per capita ranges from 5.527 to 11.676, highlighting disparities between countries.

5. **Social Support**: 
   - The average social support score stands at 0.81, implying a generally supportive environment across nations, but with a notable low of 0.228.

6. **Life Expectancy**: 
   - The average healthy life expectancy at birth is roughly 63.4 years, with a significant range between countries from 6.72 years to 74.6 years.

7. **Freedom to Make Life Choices**:
   - The mean score indicates that respondents generally perceive a moderate level of freedom, averaging around 0.75.

8. **Generosity**: 
   - Interestingly, the data suggests a potential tendency toward low levels of generosity with a mean value close to zero (9.77e-05).

9. **Perceptions of Corruption**: 
   - Researchers found that perceptions of corruption tend to be high on a scale of 0 to 1, averaging at 0.74 among populations.

10. **Positive and Negative Affect**: 
   - Positive affect averaged at about 0.65 while negative affect was significantly lower at 0.27, indicating a generally positive sentiment among respondents.

### Missing Values
A review of missing data reveals:
- **Log GDP per capita**: Missing data for 28 entries.
- **Social support**: Missing data for 13 entries.
- **Healthy life expectancy**: Missing for 63 entries.
- **Freedom to make life choices**: Missing for 36 entries.
- **Generosity**: Missing for 81 entries.
- **Perceptions of corruption**: Missing for 125 entries.

**Actionable Insight**: Addressing these missing values through imputation strategies or data collection efforts may improve the robustness of future analyses.

### Correlation Analysis
The correlation matrix presents notable relationships among key variables:
- **Strong Relationships**:
  - Life Ladder and Log GDP per capita (0.78): Suggests that higher GDP is associated with higher subjective well-being.
  - Life Ladder and Social support (0.72): Points to the impact of social relationships on well-being.
  - Life Ladder and Healthy life expectancy (0.71): Indicates that better health outcomes are linked with greater satisfaction in life.

- **Moderate Relationships**:
  - Freedom to make life choices is moderately correlated with Life Ladder (0.54) and Positive affect (0.58), stressing the importance of personal agency in well-being.

- **Negative Relationships**:
  - Life Ladder's correlation with perceptions of corruption shows a strong negative relationship (-0.43), hinting that countries perceived to have higher corruption may experience lower levels of well-being.

**Actionable Insights**:
1. **Policy Recommendations**: Governments should focus on improving economic conditions and reducing perceptions of corruption to enhance citizens' well-being.
2. **Social Programs**: Initiatives aimed at strengthening social support networks can also foster improved subjective well-being.
3. **Public Health**: Programs that promote healthy lifestyles may enhance healthy life expectancy, thereby correlating with increased life satisfaction.

### Visualizations
Visualizations created include:
- **Year Distribution**: Provides insights into the timeline of collected data.
- **Life Ladder Distribution**: Illustrates the spread of subjective well-being scores.
- **Log GDP per Capita Distribution**: Visualizes economic disparities among countries.
- **Social Support Distribution**: Highlights the levels of social connectivity and support across the dataset.
- **Correlation Heatmap**: A graphical representation of the correlation metrics which provides a clearer view of the relationships between variables.

**Actionable Insight**: Use these visualizations in reports or presentations to communicate findings more effectively to stakeholders or decision-makers.

### Conclusion
The analysis reveals critical insights into the relationship between economic indicators, health outcomes, social support, and subjective well-being. Addressing identified gaps and leveraging correlations can empower policymakers and stakeholders to design effective interventions aimed at improving quality of life across different demographic groups and countries. It is imperative to conduct follow-up assessments to track progress and adapt strategies as necessary.

![Correlation Heatmap](correlation_heatmap.png)