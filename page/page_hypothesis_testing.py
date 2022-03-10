import pandas as pd
import streamlit as st
import numpy as np
import scipy.stats as stats
import plotly.figure_factory as ff
from matplotlib import pyplot as plt


def plot_measurement(data):
    _mean = np.mean(data)
    _median = np.median(data)
    _std = np.std(data)

    fig = ff.create_distplot([data], ["Distribution"], curve_type='kde', bin_size=32)
    fig.add_vline(x=_mean, line_width=1, line_dash="dash", line_color="green")

    fig.add_vline(x=_median, line_width=1, line_dash="dash", line_color="red")

    fig.add_vline(x=_mean + _std, line_width=2, line_dash="dash", line_color="white")
    fig.add_vline(x=_mean - _std, line_width=2, line_dash="dash", line_color="white")
    return fig


def hypothesis_testing_page(df: pd.DataFrame):
    st.title("Hypothesis Testing")

    alpha = 0.05

    st.markdown(
        f"""
        > ## Hypothesis
        >> The null hypothesis is that the population mean is equal to the value of the variable of interest.  
        >> The alternative hypothesis is that the population mean is not equal to the value of the variable of interest.  
        >>  
        >> ## Background
        >>> I am interested to increase the store performance.  
        >>> I have a hypothesis that the `female` customer more likely to purchase `Health and Beauty` than `male`.   
        >>> if my assumption are true i will start new marketing campaign targeted toward `Health and Beauty` on `female` customer
        >>>
        >> ## Assumptions
        >>> Both population is normally distributed.  
        >>> The population mean is known.  
        >>> The population standard deviation is known.  
        >>> Both Variables are independent of each because they are from the different person.
        >>>
        >>> μ1 = `Male` Customer Spending on `Health and Beauty` Product  
        >>> μ2 = `Female` Customer Spending on `Health and Beauty` Product 
        >>>
        >> ### Null and Alternate Hypothesis  
        >>> H0 : μ1 = μ2  
        >>> H1 : μ1 ≠ μ2
        >>>
        >>> H0 : `Male` and `Female` Spending on `Health and Beauty` Product are the `same`   
        >>> H1 : `Male` and `Female` Spending on `Health and Beauty` Product are `not same`
        >>>
        >> ### Significance Level
        >>> The significance level is the probability of observing the null hypothesis if the null hypothesis is true.  
        >>>  
        >>> α = {alpha:.2f}  
        > ## Test Statistic
        >> The test statistic is the difference between the population mean and the value of the variable of interest.  
        >> in this case i will be using T-test for two independent samples with 2-Tailed test.
        """
    )

    col1, col2 = st.columns(2)

    df = df[df.product_line == "Health and beauty"]
    male_df = df[df.gender == "Male"]
    female_df = df[df.gender == "Female"]

    col1.markdown("## Male Spending")
    col2.markdown("## Female Spending")

    col1.markdown("""
      > From this data we can calculate the `mean` and `standard deviation` for each group and then we can create new normal distribution with
      > that property to create sample for T-Test
      """)

    col1, col2 = st.columns(2)
    col1.plotly_chart(ff.create_distplot([male_df.total.values], ["Test"], curve_type='kde', bin_size=32), use_container_width=True)
    col2.plotly_chart(ff.create_distplot([female_df.total.values], ["Test"], curve_type='kde', bin_size=32), use_container_width=True)

    st.markdown("""
          > After re-sampling from normal distribution we see that `Central Tendency` of our sample is mimicking our original distribution
      """)

    _sample_male_mean = male_df.total.mean()
    _sample_male_std = male_df.total.std()
    _sample_female_mean = female_df.total.mean()
    _sample_female_std = female_df.total.std()

    col1, col2 = st.columns(2)
    male_sample = np.random.normal(_sample_male_mean, _sample_male_std, size=512)
    female_sample = np.random.normal(_sample_female_mean, _sample_female_std, size=512)

    col1.plotly_chart(plot_measurement(male_sample), use_container_width=True)
    col2.plotly_chart(plot_measurement(female_sample), use_container_width=True)

    st.markdown("# Confidence Interval Visualisation")

    male_sample = pd.Series(male_sample)
    female_sample = pd.Series(female_sample)

    fig, ax = plt.subplots(figsize=(8 * 3, 8))
    ax.set_title("Male vs Female Spending on Health and beauty")
    ax.hist(male_sample, histtype='step', density=True, bins=64, color="blue")
    ax.hist(female_sample, histtype='step', density=True, bins=64, color="red")

    male_sample.plot.kde(ax=ax, label="Male Spending", color="blue")
    female_sample.plot.kde(ax=ax, label="Female Spending", color="red")

    lower_confidence, upper_confidence = stats.norm.interval(1 - alpha, loc=_sample_male_mean, scale=_sample_male_std)
    t_statistic, p_value = stats.ttest_ind(male_sample, female_sample)

    ax.axvline(x=lower_confidence, color="g", linestyle="--", label="Confidence Interval")
    ax.axvline(x=upper_confidence, color="g", linestyle="--")

    ax.axvline(x=_sample_male_mean + t_statistic * _sample_male_std, color="k", linestyle="--", label="Alternate Hypothesis")
    ax.axvline(x=_sample_male_mean - t_statistic * _sample_male_std, color="k", linestyle="--")
    ax.legend()
    st.pyplot(fig)

    st.markdown(f"""
      # Conclusion
      > ## Statistic Discovery
      >> The test statistic is `{t_statistic:.2f}`  
      >> The p-value is `{p_value:.2f}`  
      >>  
      >> From the p-value, we can conclude that the null hypothesis is `{'Invalid' if p_value < alpha else 'Valid'}` with a probability of `{(1 - p_value) * 100:.1f}%`  
      >>  
      >> ### Summary  
      >> We will **{'`Reject Null Hypothesis` because there are' if (p_value < alpha)
    else '`Not Reject Null Hypothesis` because there are no'} significant difference between variable**
      >> in other word we can say that `female` customer are statistically more likely to buy `Health and Beauty` product than `men` because they came from different distribution and from `Central Tendency Measurement` `Female` customer have higher average spending on `Health and Beauty` product, and soon the new targeted marketing
      >> campaign wi be started
      """)
