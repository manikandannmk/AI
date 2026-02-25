#!/usr/bin/env python3
"""
Create a comprehensive test PDF with 200+ sentences across 2 pages
for testing chunking and embedding storage
"""

import sys
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def create_comprehensive_test_pdf():
    """Create a test PDF with 2 pages and 200+ sentences"""
    
    test_pdf_path = Path("uploads/comprehensive_test.pdf")
    test_pdf_path.parent.mkdir(exist_ok=True)
    
    # Create PDF with test content
    c = canvas.Canvas(str(test_pdf_path), pagesize=letter)
    
    # Page 1 - AI and Machine Learning
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Artificial Intelligence and Machine Learning")
    
    c.setFont("Helvetica", 11)
    y_pos = 720
    line_height = 14
    
    # Page 1 content - 110+ sentences
    page1_text = """Artificial intelligence is revolutionizing the way we work and live.
Machine learning is a subset of artificial intelligence that enables computers to learn from data.
Deep learning uses neural networks to process large amounts of data.
Natural language processing allows computers to understand and generate human language.
Computer vision enables machines to interpret and understand visual information.
Supervised learning requires labeled training data for the model.
Unsupervised learning finds patterns in unlabeled data.
Reinforcement learning trains models through rewards and penalties.
Neural networks are inspired by the human brain structure.
Convolutional neural networks are used for image recognition tasks.
Recurrent neural networks process sequential data like time series.
Transformers have revolutionized natural language processing.
Transfer learning reuses pre-trained models for new tasks.
Data preprocessing is crucial for machine learning success.
Feature engineering involves selecting relevant inputs for models.
Normalization scales features to a standard range.
Dimensionality reduction reduces the number of input features.
Overfitting occurs when a model learns noise instead of patterns.
Underfitting happens when a model is too simple to capture patterns.
Cross-validation evaluates model performance on unseen data.
Hyperparameter tuning optimizes model performance.
Gradient descent is used to minimize loss functions.
Backpropagation calculates gradients for neural networks.
Activation functions introduce non-linearity to neural networks.
ReLU is a popular activation function for deep learning.
Sigmoid and tanh are used in classification tasks.
Batch normalization improves training stability.
Dropout prevents overfitting by randomly deactivating neurons.
L1 and L2 regularization add penalties to loss functions.
Early stopping prevents overfitting during training.
Learning rate controls the size of gradient updates.
Momentum accelerates convergence during training.
Adam optimizer combines momentum and adaptive learning rates.
SGD is the basic stochastic gradient descent algorithm.
Mini-batch training balances speed and accuracy.
Epoch represents one complete pass through training data.
Batch size affects training stability and efficiency.
Model evaluation uses metrics like accuracy and F1 score.
Confusion matrix shows classification performance.
ROC curves illustrate true positive versus false positive rates.
Precision measures correct positive predictions.
Recall measures detected positives among actual positives.
F1 score is the harmonic mean of precision and recall.
AUC represents the area under the ROC curve.
Mean squared error measures average prediction error.
Cross-entropy loss is used for classification tasks.
Clustering groups similar data points together.
K-means partitions data into k clusters.
Hierarchical clustering builds a tree of clusters.
DBSCAN finds clusters of arbitrary shapes.
Anomaly detection identifies unusual patterns.
Outlier detection removes extreme values from data.
Classification predicts discrete categories.
Regression predicts continuous numerical values.
Binary classification has two possible outcomes.
Multi-class classification has multiple possible outcomes.
One-hot encoding converts categories to binary vectors.
Label encoding assigns integers to categories.
Time series forecasting predicts future values.
Seasonality refers to periodic patterns in time series.
Trend represents long-term direction in data.
Stationarity means statistical properties don't change over time.
Automorphic correlation measures relationship with past values.
Moving average smooths time series data.
Exponential smoothing gives more weight to recent observations.
ARIMA combines autoregression and moving average.
Vector databases store and search embeddings efficiently.
Semantic similarity measures meaning similarity between texts.
Cosine similarity calculates angle between vectors.
Euclidean distance measures straight-line distance.
Manhattan distance measures city-block distance.
Hamming distance counts differing positions in strings.
Embeddings convert text to numerical vectors.
Word embeddings represent individual words.
Sentence embeddings represent entire sentences.
Document embeddings represent entire documents.
Skip-gram predicts context words from target word.
CBOW predicts target word from context words.
GloVe combines global matrix factorization with local context.
FastText handles out-of-vocabulary words.
BERT uses bidirectional transformer context.
GPT uses unidirectional transformer context.
T5 treats all tasks as text-to-text problems.
Attention mechanisms focus on relevant parts of input.
Multi-head attention uses multiple attention heads.
Self-attention compares words within the same sentence.
Cross-attention compares words between different sequences.
Positional encoding adds position information to embeddings.
Layer normalization standardizes activations.
Residual connections skip layers in deep networks.
Attention is all you need described the transformer architecture.
Pre-training uses large unlabeled datasets.
Fine-tuning adapts pre-trained models to specific tasks.
Zero-shot learning works without task-specific training data.
Few-shot learning works with minimal training examples.
Meta-learning learns how to learn efficiently.
Transfer learning reduces training requirements for new tasks.
Domain adaptation handles distribution shifts between datasets.
Data augmentation increases training data diversity.
Mixup interpolates between training examples.
Cutoff removes portions of input for robustness.
Adversarial training improves robustness against attacks.
Knowledge distillation transfers knowledge from large to small models."""
    
    sentences = page1_text.split('\n')
    for sentence in sentences:
        if y_pos < 80:
            c.showPage()
            c.setFont("Helvetica", 11)
            y_pos = 750
        c.drawString(50, y_pos, sentence)
        y_pos -= line_height
    
    # Page 2 content
    c.showPage()
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "Advanced Topics and Applications")
    
    c.setFont("Helvetica", 11)
    y_pos = 720
    
    page2_text = """Explainability makes machine learning models interpretable.
Feature importance shows which inputs affect predictions most.
LIME explains individual predictions.
SHAP uses game theory for model explanation.
Attention visualization shows model focus areas.
Saliency maps highlight important input regions.
Model interpretability is crucial for trust.
Fairness ensures models treat all groups equally.
Bias detection identifies unfair model behavior.
Algorithmic fairness addresses systematic discrimination.
Privacy-preserving machine learning protects sensitive data.
Differential privacy provides formal privacy guarantees.
Federated learning trains on distributed data.
Homomorphic encryption enables computation on encrypted data.
Secure multi-party computation shares computation.
Adversarial examples fool machine learning models.
Robustness testing evaluates model reliability.
Uncertainty quantification estimates prediction confidence.
Bayesian methods model uncertainty probabilistically.
Monte Carlo methods use random sampling for inference.
Variational inference approximates complex distributions.
Graph neural networks process graph-structured data.
Graph convolutional networks update node representations.
Attention layers improve graph neural networks.
Message passing exchanges information between nodes.
Node embeddings represent graph nodes.
Knowledge graphs organize information as structured data.
Entity linking connects text to knowledge bases.
Relation extraction identifies relationships between entities.
Named entity recognition identifies entities in text.
Sentiment analysis determines emotional tone.
Emotion detection identifies specific emotions.
Topic modeling discovers themes in documents.
Latent Dirichlet allocation is a topic model.
Non-negative matrix factorization factorizes data.
Recommendation systems suggest relevant items.
Collaborative filtering uses user-item interactions.
Content-based filtering uses item features.
Hybrid recommendation combines multiple approaches.
Cold start problem affects new users or items.
Exploration-exploitation balances discovering and exploiting.
Bandit algorithms select actions adaptively.
Contextual bandits use context for decisions.
Reinforcement learning trains through interaction.
Markov decision processes model sequential decisions.
Value iteration computes optimal policies.
Policy iteration finds better policies.
Q-learning learns action-value functions.
Deep Q-networks combine Q-learning with neural networks.
Policy gradient methods optimize policies directly.
Actor-critic methods combine value and policy learning.
Proximal policy optimization stabilizes policy learning.
Trust region policy optimization constrains updates.
Multi-agent reinforcement learning involves multiple learners.
Game theory analyzes strategic interactions.
Nash equilibrium is a stable game outcome.
Zero-sum games have opposite player interests.
Cooperative games allow player collaboration.
Auction mechanisms allocate resources efficiently.
Mechanism design creates incentive-compatible systems.
Blockchain enables decentralized trust.
Smart contracts automate agreement execution.
Distributed ledger technology records transactions immutably.
Consensus mechanisms achieve agreement in distributed systems.
Proof of work requires computational effort.
Proof of stake bases validation on ownership.
Byzantine fault tolerance handles arbitrary failures.
Cloud computing provides on-demand computing resources.
Edge computing brings computation closer to data.
Fog computing is an intermediate layer.
Quantum computing uses quantum phenomena.
Quantum gates manipulate quantum states.
Quantum entanglement correlates quantum systems.
Quantum superposition allows multiple states simultaneously.
Tensor networks represent quantum states.
Optimization algorithms find solutions efficiently.
Convex optimization has efficient algorithms.
Non-convex optimization is computationally harder.
Integer programming handles discrete variables.
Constraint satisfaction solves constraint problems.
Metaheuristic algorithms approximate solutions efficiently.
Genetic algorithms evolve candidate solutions.
Ant colony optimization inspired by ant behavior.
Particle swarm optimization inspired by bird flocking.
Simulated annealing mimics metal annealing.
Tabu search forbids recently visited states.
AutoML automatically designs machine learning pipelines.
Hyperparameter optimization searches parameter space.
Neural architecture search designs neural networks.
Meta-learning learns optimal learning algorithms.
Online learning adapts to streaming data.
Active learning queries most informative samples.
Semi-supervised learning uses labeled and unlabeled data.
Self-supervised learning creates labels from data.
Contrastive learning learns through similarity.
Momentum contrast builds consistent representations.
Siamese networks learn similarity metrics.
Metric learning optimizes distance functions.
Multi-task learning trains on multiple objectives.
Continual learning learns without catastrophic forgetting.
Lifelong learning accumulates knowledge over time."""
    
    sentences_page2 = page2_text.split('\n')
    for sentence in sentences_page2:
        if y_pos < 80:
            c.showPage()
            c.setFont("Helvetica", 11)
            y_pos = 750
        c.drawString(50, y_pos, sentence)
        y_pos -= line_height
    
    c.save()
    
    # Count total sentences
    total_sentences = len(sentences) + len(sentences_page2)
    print(f"✅ Created comprehensive test PDF: {test_pdf_path}")
    print(f"   Total sentences: {total_sentences}")
    print(f"   Pages: 2")
    
    return test_pdf_path


if __name__ == '__main__':
    path = create_comprehensive_test_pdf()
    print(f"\n📄 Test PDF ready at: {path}")
