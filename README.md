# Mammal World - AI for Wildlife in India

## Problem Statement

The Indian subcontinent is blessed with a diverse range of mammal species, each contributing to the region's rich biodiversity. However, wildlife conservation faces significant challenges, including the need for efficient species identification, behavior understanding, and habitat preservation. Our project addresses these challenges by harnessing AI technology to aid in wildlife conservation efforts.

## Image Collection

### Data Sources

We collected a vast dataset of images of 103 mammal species indigenous to the Indian subcontinent. The images were sourced from various wildlife databases, camera traps, and field expeditions.

### Nighttime Image Augmentation

Given that most images were captured during daylight, we employed nighttime image augmentation techniques. This involved adjusting brightness, contrast, and adding artificial noise to simulate low-light conditions, making our model robust to various lighting scenarios.

## Data Cleaning & Augmentations

We meticulously cleaned and preprocessed the collected data. This involved:

- Organizing images into a hierarchical folder structure.
- Scraping text descriptions, taxonomy, and habitat details.
- Augmenting the dataset with nighttime images.
- Annotating behaviors and actions exhibited by the species.

## Model Training

### Multimodal AI Models

We trained a multimodal AI model capable of:

- Species Identification: Accurately classifying the 103 mammal species.
- Behavior Recognition: Analyzing animal interactions, mating rituals, feeding habits, and more.
- Real-Time Monitoring: Detecting unusual behaviors or threats to wildlife.

### Training Pipeline

Our model was trained on a combination of image, text, and audio data. We used PyTorch to build custom models, incorporating state-of-the-art deep learning architectures.

## Model Deploying

Our AI models are deployed through a user-friendly web application built with Streamlit. The app provides:

- Real-time species identification.
- Behavior insights.
- Educational resources.
- Conservation updates.
- Community engagement features.

## Contributing

We welcome contributions from the community to improve and expand our project. If you have ideas, suggestions, or want to get involved, please feel free to reach out.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
