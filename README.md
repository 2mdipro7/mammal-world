# Mammal World - AI for Wildlife in India

## Table of Contents
- [Problem Statement](#problem-statement)
- [Data Collection](#data-collection)
- [Data Cleaning & Augmentations](#data-cleaning--augmentations)
- [Model Training](#model-training)
- [Model Deploying](#model-deploying)
- [Live Links](#live-links)
- [Contributing](#contributing)
- [License](#license)

## Problem Statement

The Indian subcontinent is blessed with a diverse range of mammal species, each contributing to the region's rich biodiversity. However, wildlife conservation faces significant challenges, including the need for efficient species identification, behavior understanding, and habitat preservation. Our project addresses these challenges by harnessing AI technology to aid in wildlife conservation efforts.

## Data Collection

### Data Sources

First, using selenium, we scraped all records of mammal species in the Indian subcontinent found on https://indiabiodiversity.org.

Then we collected cleaned and collected our raw text data by verifying these data from various reliable surces from the web, for example - https://animaldiversity.org.

Finally, we collected a vast dataset of images of 103 mammal species indigenous to the Indian subcontinent. The images were sourced from the web using google search engine api and the search_images_ddg() of Fastai.

### Nighttime Image Augmentation

Given that most images collected were of daytime images, we employed nighttime image augmentation techniques. This involved adjusting brightness, contrast, and adding artificial noise to simulate low-light conditions, making our model robust to various lighting scenarios.

## Data Cleaning & Augmentations

We meticulously cleaned and preprocessed the collected data. This involved:

- Organizing images into a hierarchical folder structure.
- Scraping text descriptions, taxonomy, and habitat details and relevanet information.
- Augmenting the dataset with nighttime images.
- Annotating behaviors and actions exhibited by the species.

## Model Training

### Multi-modal, Multi-target AI Model

We trained an AI model capable of:

- Species Identification: Accurately classifying the 103 mammal species.
- Behavior Recognition: Analyzing animal interactions, mating rituals, feeding habits, and more.
- Real-Time Monitoring: Detecting unusual behaviors or threats to wildlife.

### Training Pipeline

Our model was trained on a combination of image and text data. We used PyTorch and Fastai to build custom models, incorporating state-of-the-art deep learning architectures.

## Model Deploying

Our AI models are deployed through a user-friendly web application built with Streamlit. The app provides:

- Real-time species identification.
- Behavior insights.
- Educational resources.
- Conservation updates.
- Community engagement features.

## Live Links

### Huggingface model space - https://huggingface.co/spaces/dipro7/mammals-of-india

### On Streamlit - https://mammal-world.streamlit.app/

## Contributing

We welcome contributions from the community to improve and expand our project. If you have ideas, suggestions, or want to get involved, please feel free to reach out.

## Future Work


The initial aim with this project was to build a multimodal, multitarget model using image and audio as input and text as output. But due to the lack of availablity of audio data, we could not quite achieve that. If you have access to such a dataset that can be exploited for the betterment of wildlife of India, please reach out to me so we can collaborate.

A second version of the model shall have much more improved performance when it is trained on even larger number of data, and has more target labels.

The work is far from over. This is a massive project, and cannot be possiby completed as a sole member. A lot of effort required to enhance the dataset quality, expanding the target labels etc.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

If you want to be part of this project, please give me a pull request.
