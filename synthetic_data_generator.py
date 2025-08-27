import streamlit as st
import pandas as pd
import io
import base64
from sdv.single_table import GaussianCopulaSynthesizer, CTGANSynthesizer
from sdv.metadata import SingleTableMetadata
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np
import json
from datetime import datetime

def calculate_metrics(original_df, synthetic_df):
    """
    Calculate various metrics to compare original and synthetic datasets.
    """
    metrics = {}
    
    # Basic statistical metrics
    metrics['basic_stats'] = {
        'original_shape': original_df.shape,
        'synthetic_shape': synthetic_df.shape,
        'original_memory_usage': original_df.memory_usage(deep=True).sum(),
        'synthetic_memory_usage': synthetic_df.memory_usage(deep=True).sum()
    }
    
    # Data type consistency
    metrics['data_types'] = {
        'original_dtypes': original_df.dtypes.to_dict(),
        'synthetic_dtypes': synthetic_df.dtypes.to_dict()
    }
    
    # Statistical metrics for numerical columns
    numerical_cols = original_df.select_dtypes(include=['number']).columns
    metrics['numerical_metrics'] = {}
    
    for col in numerical_cols:
        orig_mean = original_df[col].mean()
        synth_mean = synthetic_df[col].mean()
        orig_std = original_df[col].std()
        synth_std = synthetic_df[col].std()
        
        # KS test for distribution similarity
        ks_stat, ks_pval = stats.ks_2samp(original_df[col], synthetic_df[col])
        
        metrics['numerical_metrics'][col] = {
            'mean_difference': abs(orig_mean - synth_mean) / orig_mean if orig_mean != 0 else 0,
            'std_difference': abs(orig_std - synth_std) / orig_std if orig_std != 0 else 0,
            'ks_statistic': ks_stat,
            'ks_pvalue': ks_pval,
            'distribution_similarity': 'Similar' if ks_pval > 0.05 else 'Different'
        }
    
    # Categorical metrics
    categorical_cols = original_df.select_dtypes(include=['object', 'category']).columns
    metrics['categorical_metrics'] = {}
    
    for col in categorical_cols:
        orig_counts = original_df[col].value_counts(normalize=True)
        synth_counts = synthetic_df[col].value_counts(normalize=True)
        
        # Calculate category distribution difference
        common_categories = set(orig_counts.index) & set(synth_counts.index)
        if common_categories:
            diff = sum(abs(orig_counts.get(cat, 0) - synth_counts.get(cat, 0)) for cat in common_categories)
            metrics['categorical_metrics'][col] = {
                'distribution_difference': diff,
                'category_coverage': len(common_categories) / len(set(orig_counts.index) | set(synth_counts.index))
            }
    
    # Correlation structure preservation
    if len(numerical_cols) > 1:
        orig_corr = original_df[numerical_cols].corr()
        synth_corr = synthetic_df[numerical_cols].corr()
        corr_diff = np.mean(np.abs(orig_corr - synth_corr))
        metrics['correlation_preservation'] = {
            'mean_correlation_difference': corr_diff,
            'correlation_preserved': corr_diff < 0.1
        }
    
    return metrics

def generate_report(metrics, original_df, synthetic_df):
    """
    Generate a comprehensive report comparing original and synthetic datasets.
    """
    report = []
    report.append("# Synthetic Data Generation Report")
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Basic Information
    report.append("## Basic Information")
    report.append(f"- Original Dataset Shape: {metrics['basic_stats']['original_shape']}")
    report.append(f"- Synthetic Dataset Shape: {metrics['basic_stats']['synthetic_shape']}")
    report.append(f"- Original Memory Usage: {metrics['basic_stats']['original_memory_usage'] / 1024:.2f} KB")
    report.append(f"- Synthetic Memory Usage: {metrics['basic_stats']['synthetic_memory_usage'] / 1024:.2f} KB\n")
    
    # Numerical Metrics
    report.append("## Numerical Metrics")
    for col, col_metrics in metrics['numerical_metrics'].items():
        report.append(f"### {col}")
        report.append(f"- Mean Difference: {col_metrics['mean_difference']*100:.2f}%")
        report.append(f"- Standard Deviation Difference: {col_metrics['std_difference']*100:.2f}%")
        report.append(f"- Distribution Similarity: {col_metrics['distribution_similarity']}")
        report.append(f"- KS Test p-value: {col_metrics['ks_pvalue']:.4f}\n")
    
    # Categorical Metrics
    if metrics['categorical_metrics']:
        report.append("## Categorical Metrics")
        for col, col_metrics in metrics['categorical_metrics'].items():
            report.append(f"### {col}")
            report.append(f"- Distribution Difference: {col_metrics['distribution_difference']*100:.2f}%")
            report.append(f"- Category Coverage: {col_metrics['category_coverage']*100:.2f}%\n")
    
    # Correlation Structure
    if 'correlation_preservation' in metrics:
        report.append("## Correlation Structure")
        report.append(f"- Mean Correlation Difference: {metrics['correlation_preservation']['mean_correlation_difference']:.4f}")
        report.append(f"- Correlation Structure Preserved: {'Yes' if metrics['correlation_preservation']['correlation_preserved'] else 'No'}\n")
    
    # Overall Assessment
    report.append("## Overall Assessment")
    numerical_similarity = np.mean([m['distribution_similarity'] == 'Similar' for m in metrics['numerical_metrics'].values()]) * 100
    categorical_similarity = np.mean([m['category_coverage'] for m in metrics['categorical_metrics'].values()]) * 100 if metrics['categorical_metrics'] else 100
    
    report.append(f"- Numerical Data Similarity: {numerical_similarity:.2f}%")
    report.append(f"- Categorical Data Similarity: {categorical_similarity:.2f}%")
    
    if 'correlation_preservation' in metrics:
        correlation_score = (1 - metrics['correlation_preservation']['mean_correlation_difference']) * 100
        report.append(f"- Correlation Structure Score: {correlation_score:.2f}%")
    
    overall_score = (numerical_similarity + categorical_similarity) / 2
    report.append(f"\nOverall Synthetic Data Quality Score: {overall_score:.2f}%")
    
    return "\n".join(report)

def generate_synthetic_data(uploaded_file, df=None):
    """
    Generate synthetic data from an uploaded CSV file or existing DataFrame.
    
    Args:
        uploaded_file: The uploaded file object from Streamlit
        df: Optional existing DataFrame if file is already loaded
        
    Returns:
        tuple: (synthetic_data, success, error_message)
    """
    try:
        # Load DataFrame appropriately
        if df is not None:
            sdg_df = df.copy()
        else:
            content = uploaded_file.read()
            if not content:
                return None, False, "The uploaded file is empty. Please upload a valid CSV file."
            sdg_df = pd.read_csv(io.BytesIO(content))

        if sdg_df.empty:
            return None, False, "The uploaded dataset is empty after loading. Please check your CSV."

        # Display original data preview
        st.subheader("📄 Original Data Preview")
        st.dataframe(sdg_df.head())

        # Choose model from available options
        model_option = st.selectbox(
            "Select Model for Data Generation",
            ("Gaussian Copula", "CTGAN"),
            key="synthetic_model_select"
        )

        col1, col2 = st.columns(2)

        with col1:
            num_samples = st.slider(
                "Number of Synthetic Data Rows",
                min_value=10,
                max_value=500,
                value=min(200, len(sdg_df)),
                step=10,
                key="synthetic_samples_slider"
            )

        with col2:
            epochs = st.slider(
                "Training Epochs",
                min_value=1,
                max_value=100,
                value=30,
                step=5,
                key="synthetic_epochs_slider"
            )

        if st.button("Generate Synthetic Data", key="generate_synthetic_button"):
            with st.spinner("Training model and generating synthetic dataset..."):
                try:
                    # Initialize metadata
                    metadata = SingleTableMetadata()
                    metadata.detect_from_dataframe(sdg_df)

                    # Initialize selected model
                    if model_option == "Gaussian Copula":
                        synthesizer = GaussianCopulaSynthesizer(metadata)
                    else:  # Use CTGAN if selected
                        synthesizer = CTGANSynthesizer(metadata)

                    # Fit model and generate synthetic data
                    synthesizer.fit(sdg_df)
                    synthetic_data = synthesizer.sample(num_rows=num_samples)

                    st.success("✅ Synthetic data generated successfully!")

                    # Calculate metrics and generate report
                    metrics = calculate_metrics(sdg_df, synthetic_data)
                    report = generate_report(metrics, sdg_df, synthetic_data)

                    # Show synthetic data preview
                    st.subheader("🔍 Synthetic Data Preview")
                    st.dataframe(synthetic_data.head())

                    # Tabs for analysis
                    st.subheader("📊 Data Analysis")
                    tab1, tab2, tab3 = st.tabs(["Statistical Summary", "Visualizations", "Quality Report"])

                    with tab1:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("Original Data Statistics")
                            st.dataframe(sdg_df.describe())
                        with col2:
                            st.write("Synthetic Data Statistics")
                            st.dataframe(synthetic_data.describe())

                    with tab2:
                        numeric_cols = sdg_df.select_dtypes(include=['number']).columns.tolist()
                        if numeric_cols:
                            selected_col = st.selectbox(
                                "Select column for distribution comparison", 
                                numeric_cols,
                                key="synthetic_distribution_select"
                            )

                            fig, ax = plt.subplots(1, 2, figsize=(12, 4))
                            sns.histplot(sdg_df[selected_col], ax=ax[0], kde=True)
                            ax[0].set_title(f"Original: {selected_col}")

                            sns.histplot(synthetic_data[selected_col], ax=ax[1], kde=True)
                            ax[1].set_title(f"Synthetic: {selected_col}")

                            st.pyplot(fig)

                            # Add correlation heatmap if multiple numerical columns
                            if len(numeric_cols) > 1:
                                st.subheader("Correlation Structure Comparison")
                                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
                                sns.heatmap(sdg_df[numeric_cols].corr(), ax=ax1, cmap='coolwarm')
                                ax1.set_title("Original Data Correlation")
                                sns.heatmap(synthetic_data[numeric_cols].corr(), ax=ax2, cmap='coolwarm')
                                ax2.set_title("Synthetic Data Correlation")
                                st.pyplot(fig)
                        else:
                            st.warning("No numerical columns available for visualization.")

                    with tab3:
                        st.markdown(report)
                        
                        # Download report
                        report_bytes = report.encode()
                        b64 = base64.b64encode(report_bytes).decode()
                        href = f'<a href="data:text/markdown;base64,{b64}" download="synthetic_data_report.md" class="btn">📥 Download Quality Report</a>'
                        st.markdown(href, unsafe_allow_html=True)

                    # Download synthetic data
                    csv = synthetic_data.to_csv(index=False)
                    b64 = base64.b64encode(csv.encode()).decode()
                    href = f'<a href="data:file/csv;base64,{b64}" download="synthetic_data.csv" class="btn">📥 Download Synthetic Data (CSV)</a>'
                    st.markdown(href, unsafe_allow_html=True)

                    return synthetic_data, True, None

                except Exception as e:
                    error_msg = f"Error generating synthetic data: {str(e)}"
                    st.error(f"❌ {error_msg}")
                    st.info("Tip: Ensure your dataset contains valid numerical/categorical columns and no null values.")
                    return None, False, error_msg

    except Exception as e:
        error_msg = f"Could not read the CSV file: {str(e)}"
        st.error(f"❌ {error_msg}")
        return None, False, error_msg
    
    # Return default values if no button was clicked
    return None, False, "Please click 'Generate Synthetic Data' to start the process." 