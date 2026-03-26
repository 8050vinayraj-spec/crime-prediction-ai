"""
CRIME PREDICTION & CYBERCRIME DETECTION SYSTEM
Code Implementations & Samples

This file contains all code implementations from the comprehensive project report,
organized by module and functionality.

Date: March 26, 2026
Version: 1.0
"""

# ============================================================================
# SECTION 1: CRIME PREDICTION MODEL IMPLEMENTATION
# ============================================================================

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
import joblib
import numpy as np
import pandas as pd


class CrimePredictionModel:
    """
    Random Forest Model for Crime Prediction across 33 Indian states/UTs
    
    Features:
    - Location encoding (33 states/UTs)
    - Monthly data (1-12)
    - Year tracking (2018-2025)
    - Historical crime counts
    
    Target: 5 crime categories
    - Theft, Assault, Cybercrime, Fraud, Vandalism
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        )
        self.le_location = LabelEncoder()
        self.le_crime = LabelEncoder()
        
    def prepare_data(self, X, y):
        """
        Prepare and encode training data
        
        Args:
            X: Feature dataframe with columns [location, month, year, historical_count]
            y: Target series with crime types
        """
        # Encode locations (33 states/UTs)
        X['location_encoded'] = self.le_location.fit_transform(X['location'])
        
        # Encode crime types
        y_encoded = self.le_crime.fit_transform(y)
        
        # Select features for training
        X_processed = X[['location_encoded', 'month', 'year', 'historical_count']]
        
        return X_processed, y_encoded
    
    def train(self, X_train, y_train, X_test=None, y_test=None):
        """
        Train the crime prediction model
        
        Args:
            X_train: Training features
            y_train: Training target
            X_test: Test features (optional)
            y_test: Test target (optional)
        """
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Calculate training accuracy
        train_accuracy = self.model.score(X_train, y_train)
        print(f"Training Accuracy: {train_accuracy:.4f}")
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_train, y_train, cv=5)
        print(f"Cross-Validation Scores: {cv_scores}")
        print(f"Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        # Test accuracy if provided
        if X_test is not None and y_test is not None:
            test_accuracy = self.model.score(X_test, y_test)
            print(f"Test Accuracy: {test_accuracy:.4f}")
            return test_accuracy
        
        return train_accuracy
    
    def predict(self, location, month, year, historical_count):
        """
        Make a crime prediction
        
        Args:
            location: State/UT name
            month: Month (1-12)
            year: Year (2018+)
            historical_count: Crime frequency in location
            
        Returns:
            Dictionary with prediction details
        """
        # Encode location
        location_encoded = self.le_location.transform([location])[0]
        
        # Prepare features
        features = np.array([[location_encoded, month, year, historical_count]])
        
        # Make prediction
        prediction_encoded = self.model.predict(features)[0]
        prediction = self.le_crime.inverse_transform([prediction_encoded])[0]
        
        # Get probability distribution
        probabilities = self.model.predict_proba(features)[0]
        probability = probabilities.max()
        
        # Get all class probabilities
        distribution = {
            self.le_crime.inverse_transform([i])[0]: prob 
            for i, prob in enumerate(probabilities)
        }
        
        # Determine confidence level
        if probability >= 0.7:
            confidence = 'High'
        elif probability >= 0.5:
            confidence = 'Medium'
        else:
            confidence = 'Low'
        
        return {
            'predicted_crime': prediction,
            'probability': float(probability),
            'confidence': confidence,
            'distribution': distribution
        }
    
    def get_feature_importance(self):
        """Get feature importance scores"""
        features = ['Location', 'Month', 'Year', 'Historical Count']
        importances = self.model.feature_importances_
        
        importance_dict = {}
        for feature, importance in zip(features, importances):
            importance_dict[feature] = float(importance)
        
        return sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
    
    def save_model(self, filepath='crime_model.pkl'):
        """Save trained model to file"""
        joblib.dump(self.model, filepath)
        joblib.dump(self.le_location, 'location_encoder.pkl')
        joblib.dump(self.le_crime, 'crime_encoder.pkl')
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='crime_model.pkl'):
        """Load trained model from file"""
        self.model = joblib.load(filepath)
        self.le_location = joblib.load('location_encoder.pkl')
        self.le_crime = joblib.load('crime_encoder.pkl')
        print(f"Model loaded from {filepath}")


# ============================================================================
# SECTION 2: PHISHING DETECTION MODEL IMPLEMENTATION
# ============================================================================

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from urllib.parse import urlparse
import re


class PhishingDetectionModel:
    """
    Gaussian Naive Bayes Model for Phishing URL Detection
    
    Features (10):
    - URL length
    - IP address presence
    - HTTPS verification
    - Suspicious keywords
    - Subdomain count
    - Domain age
    - SSL certificate
    - Page rank
    - WHOIS age
    - Redirect count
    
    Classification: Phishing (0) vs Legitimate (1)
    """
    
    def __init__(self):
        self.model = GaussianNB(var_smoothing=1e-9)
        self.feature_names = [
            'url_length',
            'has_ip',
            'has_https',
            'suspicious_keywords',
            'subdomain_count',
            'domain_age_days',
            'ssl_certificate',
            'page_rank',
            'whois_age',
            'redirect_count'
        ]
        
    def extract_features(self, url):
        """
        Extract 10 features from URL for phishing detection
        
        Args:
            url: URL string to analyze
            
        Returns:
            Dictionary with extracted features
        """
        features = {}
        
        try:
            parsed_url = urlparse(url)
            
            # Feature 1: URL length
            features['url_length'] = len(url)
            
            # Feature 2: IP address check
            ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            features['has_ip'] = 1 if re.search(ip_pattern, url) else 0
            
            # Feature 3: HTTPS check
            features['has_https'] = 1 if parsed_url.scheme == 'https' else 0
            
            # Feature 4: Suspicious keywords
            suspicious_words = [
                'verify', 'confirm', 'update', 'urgent', 'secure',
                'account', 'login', 'sign', 'bank', 'amazon', 'apple',
                'paypal', 'password', 'click', 'reward', 'claim'
            ]
            features['suspicious_keywords'] = sum(
                1 for word in suspicious_words 
                if word.lower() in url.lower()
            )
            
            # Feature 5: Subdomain count
            features['subdomain_count'] = parsed_url.netloc.count('.')
            
            # Feature 6: Domain age (simplified - 0 for new, 1 for old)
            # In production, use WHOIS API
            features['domain_age_days'] = 1540  # Placeholder
            
            # Feature 7: SSL certificate (simplified)
            features['ssl_certificate'] = 1 if parsed_url.scheme == 'https' else 0
            
            # Feature 8: Page rank (placeholder)
            features['page_rank'] = 6.5  # Placeholder
            
            # Feature 9: WHOIS age (placeholder)
            features['whois_age'] = 4  # Placeholder
            
            # Feature 10: Redirect count (placeholder)
            features['redirect_count'] = 0  # Placeholder
            
        except Exception as e:
            print(f"Error extracting features: {str(e)}")
            return None
        
        return features
    
    def prepare_features_array(self, features_dict):
        """Convert feature dictionary to numpy array for model"""
        return np.array([
            [features_dict[name] for name in self.feature_names]
        ])
    
    def train(self, X_train, y_train, X_test=None, y_test=None):
        """
        Train the phishing detection model
        
        Args:
            X_train: Training features (array)
            y_train: Training target (0=Phishing, 1=Legitimate)
            X_test: Test features (optional)
            y_test: Test target (optional)
        """
        # Train the model
        self.model.fit(X_train, y_train)
        
        # Calculate training accuracy
        train_accuracy = self.model.score(X_train, y_train)
        print(f"Training Accuracy: {train_accuracy:.4f}")
        
        # Test accuracy if provided
        if X_test is not None and y_test is not None:
            test_accuracy = self.model.score(X_test, y_test)
            print(f"Test Accuracy: {test_accuracy:.4f}")
            
            # Detailed classification report
            y_pred = self.model.predict(X_test)
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred, 
                                      target_names=['Phishing', 'Legitimate']))
            
            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            print(f"\nConfusion Matrix:\n{cm}")
            
            # ROC-AUC score
            y_pred_proba = self.model.predict_proba(X_test)[:, 1]
            roc_auc = roc_auc_score(y_test, y_pred_proba)
            print(f"ROC-AUC Score: {roc_auc:.4f}")
            
            return test_accuracy
        
        return train_accuracy
    
    def analyze_url(self, url):
        """
        Analyze URL for phishing threats
        
        Args:
            url: URL to analyze
            
        Returns:
            Dictionary with analysis results
        """
        # Extract features
        features_dict = self.extract_features(url)
        
        if features_dict is None:
            return {
                'success': False,
                'error': 'Invalid URL format'
            }
        
        # Prepare features array
        X = self.prepare_features_array(features_dict)
        
        # Make prediction
        prediction = self.model.predict(X)[0]
        probability = self.model.predict_proba(X)[0]
        
        # Classification
        if prediction == 0:
            classification = 'Phishing'
            confidence = float(probability[0])
            risk_level = 'HIGH'
            recommendation = 'Do not visit this URL - likely phishing attempt'
        else:
            classification = 'Legitimate'
            confidence = float(probability[1])
            if confidence >= 0.9:
                risk_level = 'LOW'
            elif confidence >= 0.7:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'HIGH'
            recommendation = 'URL appears safe to visit'
        
        return {
            'success': True,
            'url': url,
            'classification': classification,
            'confidence': confidence,
            'risk_level': risk_level,
            'features_analyzed': 10,
            'features': features_dict,
            'recommendations': recommendation
        }
    
    def save_model(self, filepath='phishing_model.pkl'):
        """Save trained model to file"""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='phishing_model.pkl'):
        """Load trained model from file"""
        self.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")


# ============================================================================
# SECTION 3: DJANGO VIEW IMPLEMENTATIONS
# ============================================================================

"""
Django Views for Crime Prediction and Phishing Detection

These views handle the business logic for predictions and analysis.
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import CrimeData, PhishingData
from datetime import datetime, timedelta


@login_required
@require_http_methods(["GET", "POST"])
def predict_crime(request):
    """
    Handle crime prediction requests
    
    GET: Display prediction form
    POST: Process prediction and return results
    """
    if request.method == 'GET':
        return render(request, 'crime_prediction/crime_home.html')
    
    elif request.method == 'POST':
        try:
            # Get input parameters
            state = request.POST.get('state')
            month = int(request.POST.get('month'))
            year = int(request.POST.get('year'))
            
            # Validate inputs
            if not state or not month or not year:
                return render(request, 'crime_prediction/crime_home.html', {
                    'error': 'All fields are required'
                })
            
            if month < 1 or month > 12:
                return render(request, 'crime_prediction/crime_home.html', {
                    'error': 'Month must be between 1 and 12'
                })
            
            # Check if prediction is for future
            today = datetime.now()
            pred_date = datetime(year, month, 1)
            if pred_date <= today:
                return render(request, 'crime_prediction/crime_home.html', {
                    'error': 'Predictions restricted to future dates only'
                })
            
            # Load model
            crime_model = CrimePredictionModel()
            crime_model.load_model()
            
            # Get historical crime count for location
            historical_count = CrimeData.objects.filter(
                location=state
            ).count()
            
            # Make prediction
            result = crime_model.predict(state, month, year, historical_count)
            
            # Store prediction in database
            CrimeData.objects.create(
                year=year,
                month=month,
                location=state,
                crime_type=result['predicted_crime']
            )
            
            return render(request, 'crime_prediction/crime_result.html', {
                'prediction': result['predicted_crime'],
                'probability': f"{result['probability']*100:.2f}%",
                'confidence': result['confidence'],
                'distribution': result['distribution'],
                'state': state,
                'month': month,
                'year': year
            })
            
        except Exception as e:
            return render(request, 'crime_prediction/crime_home.html', {
                'error': f'Error processing prediction: {str(e)}'
            })


@login_required
@require_http_methods(["GET", "POST"])
def analyze_phishing(request):
    """
    Handle phishing URL analysis requests
    
    GET: Display analysis form
    POST: Process URL analysis and return results
    """
    if request.method == 'GET':
        return render(request, 'cybercrime/phishing_home.html')
    
    elif request.method == 'POST':
        try:
            # Get URL input
            url = request.POST.get('url')
            
            if not url:
                return render(request, 'cybercrime/phishing_home.html', {
                    'error': 'URL field is required'
                })
            
            # Load model
            phishing_model = PhishingDetectionModel()
            phishing_model.load_model()
            
            # Analyze URL
            result = phishing_model.analyze_url(url)
            
            if not result['success']:
                return render(request, 'cybercrime/phishing_home.html', {
                    'error': result['error']
                })
            
            # Store analysis in database
            PhishingData.objects.create(
                url_length=result['features']['url_length'],
                has_ip=bool(result['features']['has_ip']),
                suspicious_keywords=result['features']['suspicious_keywords'],
                has_https=bool(result['features']['has_https']),
                result=result['classification']
            )
            
            return render(request, 'cybercrime/phishing_result.html', {
                'url': url,
                'classification': result['classification'],
                'confidence': f"{result['confidence']*100:.2f}%",
                'risk_level': result['risk_level'],
                'features': result['features'],
                'recommendation': result['recommendations']
            })
            
        except Exception as e:
            return render(request, 'cybercrime/phishing_home.html', {
                'error': f'Error analyzing URL: {str(e)}'
            })


@login_required
def crime_history(request):
    """Display prediction history"""
    predictions = CrimeData.objects.all().order_by('-recorded_at')[:100]
    
    return render(request, 'crime_prediction/crime_history.html', {
        'predictions': predictions
    })


@login_required
def phishing_history(request):
    """Display analysis history"""
    analyses = PhishingData.objects.all().order_by('-submitted_at')[:100]
    
    return render(request, 'cybercrime/phishing_history.html', {
        'analyses': analyses
    })


@login_required
def dashboard_stats(request):
    """API endpoint for dashboard statistics"""
    
    # Get statistics
    total_predictions = CrimeData.objects.count()
    total_analyses = PhishingData.objects.count()
    
    # Crime type distribution
    crime_dist = {}
    for crime_data in CrimeData.objects.all():
        crime_dist[crime_data.crime_type] = crime_dist.get(crime_data.crime_type, 0) + 1
    
    # Phishing vs legitimate
    phishing_count = PhishingData.objects.filter(result='Phishing').count()
    legitimate_count = PhishingData.objects.filter(result='Legitimate').count()
    
    return JsonResponse({
        'total_predictions': total_predictions,
        'total_analyses': total_analyses,
        'crime_distribution': crime_dist,
        'phishing_count': phishing_count,
        'legitimate_count': legitimate_count
    })


# ============================================================================
# SECTION 4: HELPER FUNCTIONS
# ============================================================================

def encode_location(state_name, states_list=None):
    """
    Encode state name to numeric value
    
    Args:
        state_name: Name of state/UT
        states_list: List of all 33 states/UTs
        
    Returns:
        Encoded integer value
    """
    if states_list is None:
        states_list = [
            'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
            'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh',
            'Jharkhand', 'Karnataka', 'Kerala', 'Madhya Pradesh',
            'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
            'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
            'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand',
            'West Bengal', 'Andaman and Nicobar', 'Chandigarh',
            'Dadra and Nagar Haveli', 'Daman and Diu', 'Delhi',
            'Lakshadweep', 'Puducherry'
        ]
    
    try:
        return states_list.index(state_name)
    except ValueError:
        return -1


def get_crime_history(state, days=365):
    """
    Get crime history for a state
    
    Args:
        state: State name
        days: Number of past days to consider
        
    Returns:
        Dictionary with crime statistics
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    crimes = CrimeData.objects.filter(
        location=state,
        recorded_at__gte=cutoff_date
    )
    
    return {
        'total': crimes.count(),
        'types': dict(crimes.values('crime_type').annotate(count=Count('id')))
    }


def validate_url(url):
    """
    Validate URL format
    
    Args:
        url: URL string
        
    Returns:
        Boolean indicating if URL is valid
    """
    url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(url_pattern, url))


# ============================================================================
# SECTION 5: UTILITY CLASSES
# ============================================================================

class ModelManager:
    """Manage ML model lifecycle"""
    
    def __init__(self):
        self.crime_model = None
        self.phishing_model = None
    
    def load_all_models(self):
        """Load all trained models"""
        self.crime_model = CrimePredictionModel()
        self.crime_model.load_model()
        
        self.phishing_model = PhishingDetectionModel()
        self.phishing_model.load_model()
    
    def save_all_models(self):
        """Save all trained models"""
        if self.crime_model:
            self.crime_model.save_model()
        
        if self.phishing_model:
            self.phishing_model.save_model()
    
    def retrain_models(self, X_crime_train, y_crime_train, 
                      X_phishing_train, y_phishing_train):
        """Retrain all models with new data"""
        print("Retraining crime model...")
        self.crime_model.train(X_crime_train, y_crime_train)
        
        print("Retraining phishing model...")
        self.phishing_model.train(X_phishing_train, y_phishing_train)
        
        self.save_all_models()


if __name__ == "__main__":
    # Example usage
    print("Crime Prediction & Cybercrime Detection System - Code Implementations")
    print("=" * 70)
    
    # Initialize models
    print("\nInitializing Crime Prediction Model...")
    crime_model = CrimePredictionModel()
    
    print("Initializing Phishing Detection Model...")
    phishing_model = PhishingDetectionModel()
    
    # Example crime prediction
    print("\n" + "=" * 70)
    print("EXAMPLE: Crime Prediction")
    print("=" * 70)
    result = crime_model.predict('Maharashtra', 3, 2026, 100)
    print(f"Predicted Crime: {result['predicted_crime']}")
    print(f"Probability: {result['probability']:.2%}")
    print(f"Confidence: {result['confidence']}")
    
    # Example phishing analysis
    print("\n" + "=" * 70)
    print("EXAMPLE: Phishing Detection")
    print("=" * 70)
    test_urls = [
        "https://secure-bank-online.tk/login",
        "https://www.google.com",
        "http://192.168.1.1/admin"
    ]
    
    for url in test_urls:
        result = phishing_model.analyze_url(url)
        if result['success']:
            print(f"\nURL: {url}")
            print(f"Classification: {result['classification']}")
            print(f"Risk Level: {result['risk_level']}")
