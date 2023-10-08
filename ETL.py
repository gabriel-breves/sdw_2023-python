{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/gabriel-breves/sdw_2023-python/blob/main/ETL.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "import pandas as pd\n",
        "\n",
        "api_url = 'https://sdw-2023-prd.up.railway.app'\n",
        "\n",
        "df = pd.read_csv('user_ids.csv')\n",
        "user_ids = df['UserID'].tolist()\n",
        "print(user_ids)"
      ],
      "metadata": {
        "id": "4VZcD6aI7KmA"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from IPython.core.async_helpers import indent\n",
        "import requests\n",
        "import json\n",
        "\n",
        "def get_user(id):\n",
        "  response = requests.get(f\"{api_url}/users/{id}\")\n",
        "  return response.json() if response.status_code == 200 else None\n",
        "\n",
        "users = [user for id in user_ids if (user := get_user(id))is not None]\n",
        "print(json.dumps(users, indent= 2))"
      ],
      "metadata": {
        "id": "VmfJgVQf7ZP5"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "!pip install openai"
      ],
      "metadata": {
        "id": "ZncduxDq7cgQ"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "\n",
        "openai_api_key = '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'"
      ],
      "metadata": {
        "id": "CcpWFXpP7j9w"
      },
      "execution_count": 16,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from openai.api_resources import completion\n",
        "import openai\n",
        "\n",
        "openai.api_key = openai_api_key\n",
        "\n",
        "def generate_ai_news(user):\n",
        "  completion = openai.ChatCompletion.create(\n",
        "      model =\"gpt-3.5-turbo\",\n",
        "      messages=[\n",
        "          {\"role\": \"system\",\n",
        "           \"content\": \"Você é um especialista em viagens\"\n",
        "           },\n",
        "\n",
        "\n",
        "          {\"role\": \"user\",\n",
        "           \"content\": f\"Crie uma mensagem para {user['name']} dizendo sobre os melhores lugares para se viajar em 2024 (máximo de 100 caracteres)\"\n",
        "          }\n",
        "      ]\n",
        "  )\n",
        "\n",
        "  return completion.choices[0].message.content.strip('\\\"')\n",
        "\n",
        "for user in users:\n",
        "  news = generate_ai_news(user)\n",
        "  print(news)\n",
        "  user['news'].append({\n",
        "      \"description\": news\n",
        "  })"
      ],
      "metadata": {
        "id": "c2rsLzYJ7moY",
        "outputId": "7c3a08e7-4e4c-4289-b360-85647d92277a",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": 21,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Descubra os melhores destinos!\n",
            "Confira os destinos imperdíveis no Brasil: Rio de Janeiro, Fernando de Noronha, Bonito, Lençóis Maranhenses, Gramado!\n",
            "Explore o mundo: praias paradisíacas, cidades históricas, montanhas deslumbrantes e muito mais!\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "def update_user(user):\n",
        "  response = requests.put(f\"{api_url}/users/{user['id']}\", json=user)\n",
        "  return True if response.status_code == 200 else False\n",
        "\n",
        "  for user in users:\n",
        "    sucesso = update_user(user)\n",
        "    print(f\"User{user['name']}\")"
      ],
      "metadata": {
        "id": "dnij8tJB7r8x"
      },
      "execution_count": 18,
      "outputs": []
    }
  ],
  "metadata": {
    "colab": {
      "name": "Olá, este é o Colaboratory",
      "provenance": [],
      "include_colab_link": true
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}